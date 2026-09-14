from database.models import AgentDecision, AuditLog, Invoice, PurchaseOrder, Vendor


def test_expected_tables_exist() -> None:
    assert Vendor.__tablename__ == "vendors"
    assert PurchaseOrder.__tablename__ == "purchase_orders"
    assert Invoice.__tablename__ == "invoices"
    assert AgentDecision.__tablename__ == "agent_decisions"
    assert AuditLog.__tablename__ == "audit_logs"
