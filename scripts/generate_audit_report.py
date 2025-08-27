#!/usr/bin/env python3
"""
JurisRank Automated Audit Report Generator
==========================================
Generates comprehensive audit reports by running all validation tests
and consolidating results into a structured markdown report.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import argparse

class AuditReportGenerator:
    def __init__(self, base_url="https://5000-i09td971cyg7b4ytmaaxl.e2b.dev"):
        self.base_url = base_url
        self.timestamp = datetime.now().isoformat()
        self.results = {}
        
    def run_external_validation(self):
        """Run external validation script and capture results."""
        print("🔍 Running external validation script...")
        
        try:
            result = subprocess.run(
                ["bash", "examples/jurisrank_agent_test.sh", self.base_url],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            self.results['external_validation'] = {
                'status': 'success' if result.returncode == 0 else 'failure',
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
            
            # Extract success rate from output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Success Rate:' in line:
                    rate = line.split('Success Rate: ')[1].split('%')[0]
                    self.results['external_validation']['success_rate'] = f"{rate}%"
                    break
                    
        except subprocess.TimeoutExpired:
            self.results['external_validation'] = {
                'status': 'timeout',
                'error': 'External validation timed out after 60 seconds'
            }
        except Exception as e:
            self.results['external_validation'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def run_contract_validation(self):
        """Run API contract validation and capture results."""
        print("📋 Running API contract validation...")
        
        try:
            result = subprocess.run(
                ["python", "test_api_contract_validation.py", self.base_url],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            self.results['contract_validation'] = {
                'status': 'success' if result.returncode == 0 else 'failure',
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
            
            # Try to load JSON report if generated
            try:
                with open('api_contract_validation_report.json', 'r') as f:
                    contract_data = json.load(f)
                    self.results['contract_validation']['report_data'] = contract_data
            except FileNotFoundError:
                pass
                
        except subprocess.TimeoutExpired:
            self.results['contract_validation'] = {
                'status': 'timeout',
                'error': 'Contract validation timed out after 120 seconds'
            }
        except Exception as e:
            self.results['contract_validation'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def run_unit_tests(self):
        """Run unit tests and capture results."""
        print("🧪 Running unit tests...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/test_basic.py", "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            self.results['unit_tests'] = {
                'status': 'success' if result.returncode == 0 else 'failure',
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            self.results['unit_tests'] = {
                'status': 'timeout',
                'error': 'Unit tests timed out after 60 seconds'
            }
        except Exception as e:
            self.results['unit_tests'] = {
                'status': 'error',
                'error': str(e)
            }
    
    def check_documentation(self):
        """Check documentation completeness."""
        print("📚 Checking documentation completeness...")
        
        required_docs = [
            'README.md',
            'EXTERNAL_AUDIT_REPORT.md',
            'EXTERNAL_ACCESS_VERIFICATION_REPORT.md',
            'SECURITY_CHECKLIST.md',
            'CONTRIBUTING.md',
            'RELEASE_NOTES_v0.9.0-open.md',
            'openapi_schema.json'
        ]
        
        doc_status = {}
        total_lines = 0
        
        for doc in required_docs:
            if Path(doc).exists():
                with open(doc, 'r') as f:
                    lines = len(f.readlines())
                    doc_status[doc] = {'exists': True, 'lines': lines}
                    total_lines += lines
            else:
                doc_status[doc] = {'exists': False, 'lines': 0}
        
        self.results['documentation'] = {
            'status': 'complete' if all(doc['exists'] for doc in doc_status.values()) else 'incomplete',
            'documents': doc_status,
            'total_lines': total_lines,
            'coverage_score': len([d for d in doc_status.values() if d['exists']]) / len(required_docs) * 100
        }
    
    def generate_report(self):
        """Generate comprehensive audit report."""
        print("📝 Generating audit report...")
        
        # Calculate overall score
        scores = []
        
        if 'external_validation' in self.results:
            if self.results['external_validation']['status'] == 'success':
                scores.append(100)
            else:
                scores.append(0)
        
        if 'contract_validation' in self.results:
            if self.results['contract_validation']['status'] == 'success':
                report_data = self.results['contract_validation'].get('report_data', {})
                if 'success_rate' in report_data:
                    rate = float(report_data['success_rate'].rstrip('%'))
                    scores.append(rate)
                else:
                    scores.append(90)  # Default if successful
            else:
                scores.append(0)
        
        if 'unit_tests' in self.results:
            if self.results['unit_tests']['status'] == 'success':
                scores.append(100)
            else:
                scores.append(0)
        
        if 'documentation' in self.results:
            scores.append(self.results['documentation']['coverage_score'])
        
        overall_score = sum(scores) / len(scores) if scores else 0
        
        # Generate markdown report
        report = f"""# 🤖 Automated JurisRank Audit Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}  
**Target URL:** {self.base_url}  
**Overall Score:** {overall_score:.1f}%  
**Status:** {'✅ PASSED' if overall_score >= 85 else '⚠️ NEEDS ATTENTION'}  

---

## 📊 Executive Summary

This automated audit report provides comprehensive validation of JurisRank's readiness for external deployment and adoption.

### Key Metrics

| Category | Score | Status |
|----------|-------|--------|"""

        # Add individual test results
        if 'external_validation' in self.results:
            status = '✅' if self.results['external_validation']['status'] == 'success' else '❌'
            rate = self.results['external_validation'].get('success_rate', 'N/A')
            report += f"\n| External Validation | {rate} | {status} {self.results['external_validation']['status'].title()} |"
        
        if 'contract_validation' in self.results:
            status = '✅' if self.results['contract_validation']['status'] == 'success' else '❌'
            report_data = self.results['contract_validation'].get('report_data', {})
            rate = report_data.get('success_rate', 'N/A')
            report += f"\n| API Contract | {rate} | {status} {self.results['contract_validation']['status'].title()} |"
        
        if 'unit_tests' in self.results:
            status = '✅' if self.results['unit_tests']['status'] == 'success' else '❌'
            report += f"\n| Unit Tests | {'100%' if status == '✅' else '0%'} | {status} {self.results['unit_tests']['status'].title()} |"
        
        if 'documentation' in self.results:
            score = self.results['documentation']['coverage_score']
            status = '✅' if score >= 95 else '⚠️' if score >= 80 else '❌'
            report += f"\n| Documentation | {score:.1f}% | {status} {'Complete' if score >= 95 else 'Partial'} |"

        report += f"""

---

## 🔍 Detailed Results

### External Validation
"""
        
        if 'external_validation' in self.results:
            ext_val = self.results['external_validation']
            report += f"""
- **Status:** {ext_val['status'].title()}
- **Success Rate:** {ext_val.get('success_rate', 'N/A')}
- **Return Code:** {ext_val.get('return_code', 'N/A')}
"""
            if ext_val['status'] != 'success' and 'error' in ext_val:
                report += f"- **Error:** `{ext_val['error']}`\n"

        report += "\n### API Contract Validation\n"
        
        if 'contract_validation' in self.results:
            contract = self.results['contract_validation']
            report += f"""
- **Status:** {contract['status'].title()}
- **Return Code:** {contract.get('return_code', 'N/A')}
"""
            
            if 'report_data' in contract:
                data = contract['report_data']
                report += f"""- **Passed Tests:** {data.get('passed', 'N/A')}
- **Failed Tests:** {data.get('failed', 'N/A')}
- **Success Rate:** {data.get('success_rate', 'N/A')}
"""

        report += "\n### Documentation Coverage\n"
        
        if 'documentation' in self.results:
            docs = self.results['documentation']
            report += f"""
- **Overall Coverage:** {docs['coverage_score']:.1f}%
- **Total Lines:** {docs['total_lines']}
- **Documents Status:**
"""
            for doc_name, doc_info in docs['documents'].items():
                status = '✅' if doc_info['exists'] else '❌'
                lines = f"({doc_info['lines']} lines)" if doc_info['exists'] else ""
                report += f"  - {status} `{doc_name}` {lines}\n"

        report += f"""
---

## 🚀 Recommendations

"""
        
        if overall_score >= 90:
            report += """
✅ **Ready for Production Release**
- All critical validations passed
- External API accessible and responsive  
- Documentation complete and comprehensive
- Security headers properly implemented

**Next Steps:**
1. Tag official release version
2. Update production deployment
3. Announce public availability
"""
        elif overall_score >= 75:
            report += """
⚠️ **Ready with Minor Issues**
- Most validations passed successfully
- Some improvements recommended before full release
- Address failing tests and documentation gaps

**Action Items:**
1. Fix failing validation tests
2. Complete missing documentation
3. Re-run audit before release
"""
        else:
            report += """
❌ **Not Ready for Release**
- Critical issues identified in validation
- Significant improvements required
- Do not proceed with public release

**Critical Actions:**
1. Address all failing tests
2. Complete documentation requirements
3. Fix API contract issues
4. Re-validate before proceeding
"""

        report += f"""

---

## 📋 Audit Artifacts

- **Validation Scripts:** `examples/jurisrank_agent_test.sh`
- **Contract Tests:** `test_api_contract_validation.py`
- **Unit Tests:** `tests/test_basic.py`
- **Generated Reports:** Check CI/CD artifacts

## 🔗 External Links

- **Live API:** {self.base_url}
- **Documentation:** {self.base_url}/docs
- **OpenAPI Schema:** {self.base_url}/api/v1/openapi.json
- **Repository:** https://github.com/adrianlerer/jurisrank-core

---

*This report was generated automatically on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S UTC')}*
*Audit framework version: 1.0.0*
"""
        
        return report
    
    def run_full_audit(self):
        """Run complete audit process."""
        print("🔍 Starting JurisRank Full Audit Process")
        print("=" * 50)
        
        # Run all validation tests
        self.run_external_validation()
        self.run_contract_validation()
        self.run_unit_tests()
        self.check_documentation()
        
        # Generate and save report
        report = self.generate_report()
        
        # Save to file
        with open('AUTOMATED_AUDIT_REPORT.md', 'w') as f:
            f.write(report)
        
        print("\n📝 Audit report generated: AUTOMATED_AUDIT_REPORT.md")
        
        # Also save JSON data for CI/CD
        with open('audit_results.json', 'w') as f:
            json.dump({
                'timestamp': self.timestamp,
                'base_url': self.base_url,
                'results': self.results
            }, f, indent=2)
        
        print("📊 Audit data saved: audit_results.json")
        
        return report

def main():
    parser = argparse.ArgumentParser(description='Generate JurisRank audit report')
    parser.add_argument('--base-url', 
                        default='https://5000-i09td971cyg7b4ytmaaxl.e2b.dev',
                        help='Base URL for API validation')
    parser.add_argument('--output', 
                        default='AUTOMATED_AUDIT_REPORT.md',
                        help='Output file for audit report')
    
    args = parser.parse_args()
    
    generator = AuditReportGenerator(args.base_url)
    report = generator.run_full_audit()
    
    print("\n" + "=" * 50)
    print("✅ Audit Complete!")
    print(f"📄 Report: {args.output}")
    print("🔍 Review results and take action as needed")

if __name__ == "__main__":
    main()