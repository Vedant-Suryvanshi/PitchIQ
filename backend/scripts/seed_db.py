# backend/scripts/seed_db.py
"""
Seed database with sample data for testing
"""

import asyncio
import uuid
import random
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from database import AsyncSessionLocal
from models import MemoJob, MemoResult, User, JobStatus
import structlog

logger = structlog.get_logger(__name__)

# Sample data
SAMPLE_STARTUPS = [
    {
        "name": "AI Legal Tech",
        "industry": "Legal Tech",
        "description": "AI-powered contract review platform for small businesses",
        "status": "completed"
    },
    {
        "name": "MediScan AI",
        "industry": "Healthcare",
        "description": "Computer vision for medical image analysis",
        "status": "completed"
    },
    {
        "name": "EcoTrack",
        "industry": "Sustainability",
        "description": "Carbon footprint tracking for enterprises",
        "status": "running"
    },
    {
        "name": "FinGuard",
        "industry": "Fintech",
        "description": "AI fraud detection for banking",
        "status": "completed"
    },
    {
        "name": "AgriSense",
        "industry": "Agriculture",
        "description": "IoT sensors for smart farming",
        "status": "failed"
    }
]

SAMPLE_USERS = [
    {"username": "founder1", "email": "founder1@example.com"},
    {"username": "founder2", "email": "founder2@example.com"},
    {"username": "investor1", "email": "investor1@example.com"},
]


async def seed_users():
    """Seed users table with sample data."""
    async with AsyncSessionLocal() as session:
        for user_data in SAMPLE_USERS:
            # Check if user exists
            from sqlalchemy import select
            stmt = select(User).where(User.email == user_data["email"])
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if not existing:
                user = User(
                    id=str(uuid.uuid4()),
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password="hashed_password_placeholder",  # Will be updated later
                    is_active=True
                )
                session.add(user)
                logger.info("seed.user_created", username=user_data["username"])
        
        await session.commit()
        logger.info("seed.users_completed", count=len(SAMPLE_USERS))


async def seed_memos():
    """Seed memo_jobs and memo_results with sample data."""
    async with AsyncSessionLocal() as session:
        for i, startup in enumerate(SAMPLE_STARTUPS):
            # Create job
            job_id = str(uuid.uuid4())
            created_at = datetime.utcnow() - timedelta(days=random.randint(0, 30))
            updated_at = created_at + timedelta(minutes=random.randint(1, 60))
            
            job = MemoJob(
                id=job_id,
                startup_description=startup["description"],
                status=JobStatus(startup["status"]),
                created_at=created_at,
                updated_at=updated_at
            )
            session.add(job)
            
            # If completed, create result
            if startup["status"] == "completed":
                confidence = round(random.uniform(0.7, 0.95), 2)
                result = MemoResult(
                    id=str(uuid.uuid4()),
                    job_id=job_id,
                    startup_name=startup["name"],
                    industry=startup["industry"],
                    business_model="SaaS" if random.random() > 0.5 else "B2B",
                    target_users="Enterprises" if random.random() > 0.5 else "SMBs",
                    geography="Global",
                    market_research_output=f"Market research for {startup['name']}...",
                    funding_analysis_output=f"Funding analysis for {startup['name']}...",
                    memo_markdown=f"# Investor Memo\n\n## Executive Summary\n\n{startup['name']} is building...",
                    confidence_score=confidence,
                    quality_flags={"flags": []},
                    created_at=created_at
                )
                session.add(result)
                logger.info("seed.memo_created", name=startup["name"], confidence=confidence)
        
        await session.commit()
        logger.info("seed.memos_completed", count=len(SAMPLE_STARTUPS))


async def seed_all():
    """Run all seed operations."""
    logger.info("seed.starting")
    
    try:
        # Check if tables exist
        async with AsyncSessionLocal() as session:
            from sqlalchemy import text
            result = await session.execute(text("SELECT COUNT(*) FROM memo_jobs"))
            count = result.scalar()
            
            if count > 0:
                logger.info("seed.skip", reason="Data already exists", count=count)
                return
        
        await seed_users()
        await seed_memos()
        
        logger.info("seed.completed")
        
    except Exception as e:
        logger.error("seed.failed", error=str(e))
        raise


async def clear_all():
    """Clear all data from tables."""
    async with AsyncSessionLocal() as session:
        from sqlalchemy import text
        await session.execute(text("TRUNCATE TABLE memo_results CASCADE"))
        await session.execute(text("TRUNCATE TABLE memo_jobs CASCADE"))
        await session.execute(text("TRUNCATE TABLE users CASCADE"))
        await session.commit()
        logger.info("seed.cleared")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Database seed tool")
    parser.add_argument("action", choices=["seed", "clear", "reset"],
                       help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "seed":
        asyncio.run(seed_all())
    elif args.action == "clear":
        asyncio.run(clear_all())
    elif args.action == "reset":
        confirm = input("⚠️  This will delete all data! Are you sure? (yes/no): ")
        if confirm.lower() == "yes":
            asyncio.run(clear_all())
            asyncio.run(seed_all())
            print("✅ Database reset and seeded!")
        else:
            print("Operation cancelled")


if __name__ == "__main__":
    main()