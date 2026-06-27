# backend/scripts/db_health.py
"""
Database health check script
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from database import AsyncSessionLocal, test_connection, get_db_stats
from sqlalchemy import text
import structlog

logger = structlog.get_logger(__name__)


async def check_health():
    """Check database health and return status."""
    results = {
        "status": "healthy",
        "checks": {}
    }
    
    # Check 1: Connection
    connection_ok = await test_connection()
    results["checks"]["connection"] = connection_ok
    if not connection_ok:
        results["status"] = "unhealthy"
        logger.error("health.check.failed", check="connection")
    
    # Check 2: Query execution
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            query_ok = result.scalar() == 1
            results["checks"]["query_execution"] = query_ok
            if not query_ok:
                results["status"] = "unhealthy"
                logger.error("health.check.failed", check="query_execution")
    except Exception as e:
        results["checks"]["query_execution"] = False
        results["status"] = "unhealthy"
        logger.error("health.check.failed", check="query_execution", error=str(e))
    
    # Check 3: Tables exist
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('memo_jobs', 'memo_results', 'users')
            """))
            tables_count = result.scalar()
            tables_ok = tables_count >= 3
            results["checks"]["tables_exist"] = tables_ok
            results["tables_found"] = tables_count
            if not tables_ok:
                results["status"] = "warning"
                logger.warning("health.check.missing_tables", count=tables_count)
    except Exception as e:
        results["checks"]["tables_exist"] = False
        results["status"] = "unhealthy"
        logger.error("health.check.failed", check="tables_exist", error=str(e))
    
    # Check 4: Connection stats
    try:
        stats = await get_db_stats()
        results["checks"]["connection_stats"] = True
        results["stats"] = stats
    except Exception as e:
        results["checks"]["connection_stats"] = False
        logger.warning("health.check.stats_failed", error=str(e))
    
    # Determine overall health
    if results["status"] == "healthy":
        logger.info("health.check.passed")
    else:
        logger.warning("health.check.failed", status=results["status"])
    
    return results


async def main():
    """Main entry point."""
    import json
    
    results = await check_health()
    print(json.dumps(results, indent=2, default=str))
    
    # Exit with appropriate code
    if results["status"] == "healthy":
        sys.exit(0)
    elif results["status"] == "warning":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    asyncio.run(main())