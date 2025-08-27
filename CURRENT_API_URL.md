# 🌐 Current JurisRank API URL

**Active API Endpoint:** https://5000-ihpc0zttjgtqrprr5t3vr.e2b.dev

## 🔍 Quick Validation

### Test Health Endpoint
```bash
curl -sS https://5000-ihpc0zttjgtqrprr5t3vr.e2b.dev/health
```

### Test API Status
```bash
curl -sS https://5000-ihpc0zttjgtqrprr5t3vr.e2b.dev/api/v1/status
```

### View API Documentation
- **Swagger UI:** https://5000-ihpc0zttjgtqrprr5t3vr.e2b.dev/docs
- **OpenAPI Schema:** https://5000-ihpc0zttjgtqrprr5t3vr.e2b.dev/api/v1/openapi.json

## 🧪 Complete External Validation

```bash
# Run full external validation test
bash <(curl -fsSL https://raw.githubusercontent.com/adrianlerer/jurisrank-core/main/examples/jurisrank_agent_test.sh) https://5000-ihpc0zttjgtqrprr5t3vr.e2b.dev
```

**Expected Result:** 🎉 100% Success Rate (7/7 tests passed)

## 📊 Local Verification

```bash
# From your local jurisrank-core directory
python3 verify_setup.py
```

**Expected Result:** ✅ Ready for development and external use (100% score)

---

*Updated: 2025-08-27 20:25 UTC*  
*Status: ✅ Operational and validated*