from fastapi import FastAPI, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from decimal import Decimal
import uvicorn
import logging
import asyncio
from sqlalchemy import create_engine, Column, Integer, String, Numeric, select
from sqlalchemy.orm import declarative_base, sessionmaker

# Configuração de Logs estruturados
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("finance_api")

DATABASE_URL = "sqlite:///./demo_finance.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    name = Column(String)
    balance = Column(Numeric(12, 2))

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, index=True)
    account_id = Column(Integer)
    description = Column(String)
    amount = Column(Numeric(12, 2))
    type = Column(String) # 'credit' | 'debit'

# Criação das tabelas
Base.metadata.create_all(bind=engine)

# População inicial (Seed)
db = SessionLocal()
if db.query(Account).count() == 0:
    # Contas do Tenant 1
    db.add(Account(id=1, tenant_id=1, name="Primary Account", balance=Decimal("150.00")))
    db.add(Account(id=2, tenant_id=1, name="Savings Account", balance=Decimal("50.00")))
    
    # Contas do Tenant 2 (Simulando isolamento anti-IDOR)
    db.add(Account(id=3, tenant_id=2, name="External Account (Tenant 2)", balance=Decimal("1000.00")))
    db.add(Account(id=4, tenant_id=2, name="Savings Account (Tenant 2)", balance=Decimal("500.00")))
    
    # Transações iniciais
    db.add(Transaction(tenant_id=1, account_id=1, description="Salary Payment", amount=Decimal("200.00"), type="credit"))
    db.add(Transaction(tenant_id=1, account_id=1, description="AWS Cloud Services", amount=Decimal("50.00"), type="debit"))
    db.add(Transaction(tenant_id=2, account_id=3, description="Initial Deposit", amount=Decimal("1000.00"), type="credit"))
    db.commit()
db.close()

app = FastAPI(title="Claude Code Self-Refined Backend Demo")

# Habilitando CORS para comunicação com o Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransferRequest(BaseModel):
    from_account_id: int = Field(..., gt=0)
    to_account_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., gt=0, decimal_places=2, max_digits=12)

# Endpoints
@app.get("/api/accounts")
async def get_accounts(x_tenant_id: int = Header(default=1)):
    db = SessionLocal()
    try:
        accounts = db.query(Account).filter(Account.tenant_id == x_tenant_id).all()
        return accounts
    finally:
        db.close()

@app.get("/api/accounts/{account_id}/transactions")
async def get_transactions(account_id: int, x_tenant_id: int = Header(default=1)):
    db = SessionLocal()
    try:
        # Verifica se a conta pertence ao Tenant (Proteção contra IDOR)
        account = db.query(Account).filter(Account.id == account_id, Account.tenant_id == x_tenant_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found in this tenant.")
            
        transactions = db.query(Transaction).filter(
            Transaction.account_id == account_id, 
            Transaction.tenant_id == x_tenant_id
        ).order_by(Transaction.id.desc()).limit(3).all()
        return transactions
    finally:
        db.close()

@app.post("/api/transfer")
async def execute_transfer(payload: TransferRequest, x_tenant_id: int = Header(default=1)):
    # Simulação de latência de rede
    await asyncio.sleep(1.0)
    
    if payload.from_account_id == payload.to_account_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source and destination accounts must be different."
        )

    db = SessionLocal()
    try:
        # Usamos uma transação para garantir atomicidade
        db.begin()
        
        # SELECT FOR UPDATE para evitar condições de corrida (Race Conditions)
        # SQLite não suporta FOR UPDATE clássico, mas o lock de transação do begin() em modo estrito cuida disso.
        from_account = db.query(Account).filter(
            Account.id == payload.from_account_id, 
            Account.tenant_id == x_tenant_id
        ).with_for_update().first()
        
        to_account = db.query(Account).filter(
            Account.id == payload.to_account_id, 
            Account.tenant_id == x_tenant_id
        ).with_for_update().first()

        if not from_account or not to_account:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or both accounts were not found in this tenant."
            )

        if from_account.balance < payload.amount:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance in source account."
            )

        # Processamento atômico de saldo
        from_account.balance -= payload.amount
        to_account.balance += payload.amount

        # Registra histórico de transações
        db.add(Transaction(
            tenant_id=x_tenant_id,
            account_id=from_account.id,
            description=f"Transfer to {to_account.name}",
            amount=payload.amount,
            type="debit"
        ))
        db.add(Transaction(
            tenant_id=x_tenant_id,
            account_id=to_account.id,
            description=f"Transfer from {from_account.name}",
            amount=payload.amount,
            type="credit"
        ))

        db.commit()
        logger.info("transfer_success", extra={
            "tenant_id": x_tenant_id,
            "from_account": from_account.id,
            "to_account": to_account.id,
            "amount": str(payload.amount)
        })
        return {"status": "success", "amount": float(payload.amount)}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error("transfer_failed", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Transactional database error."
        )
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
