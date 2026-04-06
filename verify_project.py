"""
Project verification script - checks if all required files and components are present
"""
import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - MISSING")
        return False

def verify_project():
    """Verify all project components"""
    print("=" * 70)
    print("Finance Data Processing Backend - Project Verification")
    print("=" * 70)
    print()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    all_checks = []
    
    # Core files
    print("📋 Core Files:")
    all_checks.append(check_file_exists(os.path.join(base_dir, "requirements.txt"), "requirements.txt"))
    all_checks.append(check_file_exists(os.path.join(base_dir, ".env.example"), ".env.example"))
    all_checks.append(check_file_exists(os.path.join(base_dir, ".gitignore"), ".gitignore"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "seed_data.py"), "seed_data.py"))
    print()
    
    # Documentation
    print("📚 Documentation:")
    all_checks.append(check_file_exists(os.path.join(base_dir, "README.md"), "README.md"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "QUICKSTART.md"), "QUICKSTART.md"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "API_DOCS.md"), "API_DOCS.md"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "ARCHITECTURE.md"), "ARCHITECTURE.md"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "PROJECT_SUMMARY.md"), "PROJECT_SUMMARY.md"))
    print()
    
    # Application structure
    print("🏗️ Application Structure:")
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "main.py"), "app/main.py"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "database.py"), "app/database.py"))
    print()
    
    # Models
    print("💾 Database Models:")
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "models", "user.py"), "app/models/user.py"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "models", "financial_record.py"), "app/models/financial_record.py"))
    print()
    
    # Schemas
    print("📝 Pydantic Schemas:")
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "schemas", "user.py"), "app/schemas/user.py"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "schemas", "financial_record.py"), "app/schemas/financial_record.py"))
    print()
    
    # Routers
    print("🛣️ API Routers:")
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "routers", "auth.py"), "app/routers/auth.py"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "routers", "users.py"), "app/routers/users.py"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "routers", "financial_records.py"), "app/routers/financial_records.py"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "routers", "dashboard.py"), "app/routers/dashboard.py"))
    print()
    
    # Services
    print("⚙️ Business Logic Services:")
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "services", "user_service.py"), "app/services/user_service.py"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "services", "financial_service.py"), "app/services/financial_service.py"))
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "services", "dashboard_service.py"), "app/services/dashboard_service.py"))
    print()
    
    # Middleware
    print("🔒 Middleware:")
    all_checks.append(check_file_exists(os.path.join(base_dir, "app", "middleware", "auth_middleware.py"), "app/middleware/auth_middleware.py"))
    print()
    
    # Summary
    print("=" * 70)
    passed = sum(all_checks)
    total = len(all_checks)
    print(f"Verification Complete: {passed}/{total} checks passed")
    
    if passed == total:
        print("✅ All components are present and accounted for!")
        print("\n🚀 Project is ready to run!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Setup PostgreSQL database")
        print("3. Configure .env file")
        print("4. Run seed script: python seed_data.py")
        print("5. Start server: python -m app.main")
        print("6. Access API docs: http://localhost:8000/docs")
        return 0
    else:
        print(f"❌ {total - passed} components are missing!")
        print("Please ensure all files are present before running the application.")
        return 1

if __name__ == "__main__":
    sys.exit(verify_project())
