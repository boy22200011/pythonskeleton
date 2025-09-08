class Config:
    def __init__(self, env: str = "dev"):
        self.env = env
        if env == "dev":
            self.db_conn = "mysql://user:pass@localhost:3306/devdb"
        elif env == "test":
            self.db_conn = "mysql://user:pass@localhost:3306/testdb"
        else:  # prod
            self.db_conn = "mysql://user:pass@dbserver:3306/proddb"

__all__ = ["Config"]