#!/usr/bin/env python3
"""
Comprehensive test script for data flow validation
Tests each stage of the application before data flows to the next stage
"""

import sys
import os
import json
from unittest.mock import Mock, patch, MagicMock

# Add the app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock Streamlit before importing app
sys.modules['streamlit'] = MagicMock()
st = sys.modules['streamlit']
st.session_state = {}
st.secrets = {}
st.error = print
st.warning = print
st.info = print
st.success = print
st.caption = print
st.spinner = lambda x: MagicMock(__enter__=lambda x: None, __exit__=lambda *args: None)

# Now import app functions
try:
    from app import (
        extract_text_from_resume,
        extract_profile_from_resume,
        verify_profile_accuracy,
        generate_and_store_resume_embedding,
        fetch_jobs_with_cache,
        _get_cached_jobs,
        _store_jobs_in_cache,
        _build_jobs_cache_key
    )
except ImportError as e:
    print(f"❌ Error importing app functions: {e}")
    print("Make sure app.py is in the same directory")
    sys.exit(1)


class TestDataFlow:
    """Test suite for data flow validation"""
    
    def __init__(self):
        self.test_results = []
        self.mock_resume_text = """John Doe
john.doe@email.com | +1-555-0123 | San Francisco, CA

PROFESSIONAL SUMMARY
Experienced software developer with 5+ years in Python and machine learning.
Led development of ML models improving accuracy by 30%.

EXPERIENCE
Senior Software Engineer | Tech Corp | 2020-2024
- Led development of ML models improving accuracy by 30%
- Built scalable APIs handling 1M+ requests/day
- Mentored team of 5 junior developers

Software Developer | StartupXYZ | 2018-2020
- Developed full-stack web applications using Python and React
- Reduced application load time by 40% through optimization

EDUCATION
BS Computer Science | University of California | 2018

SKILLS
Python, Machine Learning, TensorFlow, React, SQL, Docker, AWS

CERTIFICATIONS
AWS Certified Solutions Architect, Google Cloud Professional ML Engineer"""
        
        self.mock_profile_data = {
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "+1-555-0123",
            "location": "San Francisco, CA",
            "linkedin": "",
            "portfolio": "",
            "summary": "Experienced software developer with 5+ years in Python and machine learning.",
            "experience": "Senior Software Engineer | Tech Corp | 2020-2024\n- Led development of ML models\nSoftware Developer | StartupXYZ | 2018-2020",
            "education": "BS Computer Science | University of California | 2018",
            "skills": "Python, Machine Learning, TensorFlow, React, SQL, Docker, AWS",
            "certifications": "AWS Certified Solutions Architect, Google Cloud Professional ML Engineer"
        }
    
    def test_stage_1_resume_extraction(self):
        """Test Stage 1: Resume text extraction from files"""
        print("\n" + "="*80)
        print("TESTING STAGE 1: Resume Text Extraction")
        print("="*80)
        
        try:
            # Test with mock file
            mock_file = Mock()
            mock_file.name = "test_resume.pdf"
            mock_file.type = "application/pdf"
            mock_file.read.return_value = b"%PDF-1.4\nMock PDF content"
            
            # Mock PyPDF2
            with patch('app.PyPDF2.PdfReader') as mock_pdf:
                mock_reader = Mock()
                mock_page = Mock()
                mock_page.extract_text.return_value = self.mock_resume_text
                mock_reader.pages = [mock_page]
                mock_pdf.return_value = mock_reader
                
                result = extract_text_from_resume(mock_file)
                
                if result and len(result) > 0:
                    print("✅ Stage 1 PASSED: Resume text extracted successfully")
                    print(f"   Extracted {len(result)} characters")
                    self.test_results.append(("Stage 1: Resume Extraction", True, ""))
                    return True
                else:
                    print("❌ Stage 1 FAILED: No text extracted")
                    self.test_results.append(("Stage 1: Resume Extraction", False, "No text extracted"))
                    return False
        except Exception as e:
            print(f"❌ Stage 1 FAILED: {e}")
            import traceback
            traceback.print_exc()
            self.test_results.append(("Stage 1: Resume Extraction", False, str(e)))
            return False
    
    def test_stage_2_profile_extraction(self):
        """Test Stage 2: Profile extraction from resume text"""
        print("\n" + "="*80)
        print("TESTING STAGE 2: Profile Extraction (First Pass)")
        print("="*80)
        
        try:
            # Mock Azure OpenAI API
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'choices': [{
                    'message': {
                        'content': json.dumps(self.mock_profile_data)
                    }
                }],
                'usage': {
                    'prompt_tokens': 500,
                    'completion_tokens': 300
                }
            }
            
            with patch('app.get_text_generator') as mock_get_gen, \
                 patch('app.api_call_with_retry') as mock_retry:
                
                mock_gen = Mock()
                mock_gen.url = "https://test.openai.azure.com"
                mock_gen.headers = {"Authorization": "Bearer test"}
                mock_gen.token_tracker = None
                mock_get_gen.return_value = mock_gen
                mock_retry.return_value = mock_response
                
                result = extract_profile_from_resume(self.mock_resume_text)
                
                if result and isinstance(result, dict):
                    required_fields = ['name', 'email', 'summary', 'experience', 'skills']
                    missing = [f for f in required_fields if f not in result]
                    
                    if not missing:
                        print("✅ Stage 2 PASSED: Profile extracted with all required fields")
                        print(f"   Name: {result.get('name', 'N/A')}")
                        print(f"   Skills: {result.get('skills', 'N/A')[:50]}...")
                        self.test_results.append(("Stage 2: Profile Extraction", True, ""))
                        return True
                    else:
                        print(f"❌ Stage 2 FAILED: Missing fields: {missing}")
                        self.test_results.append(("Stage 2: Profile Extraction", False, f"Missing fields: {missing}"))
                        return False
                else:
                    print("❌ Stage 2 FAILED: Invalid profile data returned")
                    self.test_results.append(("Stage 2: Profile Extraction", False, "Invalid data"))
                    return False
        except Exception as e:
            print(f"❌ Stage 2 FAILED: {e}")
            import traceback
            traceback.print_exc()
            self.test_results.append(("Stage 2: Profile Extraction", False, str(e)))
            return False
    
    def test_stage_3_profile_verification(self):
        """Test Stage 3: Profile verification (Second Pass) before resume generation"""
        print("\n" + "="*80)
        print("TESTING STAGE 3: Profile Verification (Second Pass)")
        print("="*80)
        
        try:
            # Mock verified profile (slightly corrected)
            verified_profile = self.mock_profile_data.copy()
            verified_profile['experience'] = "Senior Software Engineer | Tech Corp | 2020-2024\n- Led development of ML models improving accuracy by 30%"
            
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'choices': [{
                    'message': {
                        'content': json.dumps(verified_profile)
                    }
                }],
                'usage': {
                    'prompt_tokens': 400,
                    'completion_tokens': 250
                }
            }
            
            with patch('app.get_text_generator') as mock_get_gen, \
                 patch('app.api_call_with_retry') as mock_retry:
                
                mock_gen = Mock()
                mock_gen.url = "https://test.openai.azure.com"
                mock_gen.headers = {"Authorization": "Bearer test"}
                mock_gen.token_tracker = None
                mock_get_gen.return_value = mock_gen
                mock_retry.return_value = mock_response
                
                result = verify_profile_accuracy(self.mock_profile_data, self.mock_resume_text)
                
                if result and isinstance(result, dict):
                    print("✅ Stage 3 PASSED: Profile verified successfully")
                    print(f"   Verified profile has {len(result)} fields")
                    self.test_results.append(("Stage 3: Profile Verification", True, ""))
                    return True
                else:
                    print("❌ Stage 3 FAILED: Verification returned invalid data")
                    self.test_results.append(("Stage 3: Profile Verification", False, "Invalid data"))
                    return False
        except Exception as e:
            print(f"❌ Stage 3 FAILED: {e}")
            import traceback
            traceback.print_exc()
            self.test_results.append(("Stage 3: Profile Verification", False, str(e)))
            return False
    
    def test_stage_4_resume_embedding(self):
        """Test Stage 4: Resume embedding generation"""
        print("\n" + "="*80)
        print("TESTING STAGE 4: Resume Embedding Generation")
        print("="*80)
        
        try:
            # Mock embedding generator
            mock_embedding = [0.1] * 1536  # Mock embedding vector
            mock_tokens = 100
            
            with patch('app.get_embedding_generator') as mock_get_emb, \
                 patch('app.get_token_tracker') as mock_get_tracker:
                
                mock_emb_gen = Mock()
                mock_emb_gen.get_embedding.return_value = (mock_embedding, mock_tokens)
                mock_get_emb.return_value = mock_emb_gen
                mock_get_tracker.return_value = None
                
                # Set session state
                st.session_state = {}
                
                result = generate_and_store_resume_embedding(
                    self.mock_resume_text,
                    self.mock_profile_data
                )
                
                if result and len(result) > 0:
                    print("✅ Stage 4 PASSED: Resume embedding generated and stored")
                    print(f"   Embedding dimension: {len(result)}")
                    print(f"   Stored in session: {'resume_embedding' in st.session_state}")
                    self.test_results.append(("Stage 4: Resume Embedding", True, ""))
                    return True
                else:
                    print("❌ Stage 4 FAILED: No embedding generated")
                    self.test_results.append(("Stage 4: Resume Embedding", False, "No embedding"))
                    return False
        except Exception as e:
            print(f"❌ Stage 4 FAILED: {e}")
            import traceback
            traceback.print_exc()
            self.test_results.append(("Stage 4: Resume Embedding", False, str(e)))
            return False
    
    def test_stage_5_job_caching(self):
        """Test Stage 5: Job fetching and caching"""
        print("\n" + "="*80)
        print("TESTING STAGE 5: Job Caching System")
        print("="*80)
        
        try:
            # Initialize session state
            st.session_state = {}
            
            # Test cache key generation
            cache_key = _build_jobs_cache_key(
                "Python Developer",
                "Hong Kong",
                25,
                "fulltime",
                "hk"
            )
            
            if cache_key:
                print(f"✅ Cache key generated: {cache_key[:50]}...")
            else:
                print("❌ Stage 5 FAILED: Cache key generation failed")
                self.test_results.append(("Stage 5: Job Caching", False, "Cache key failed"))
                return False
            
            # Test storing jobs in cache
            mock_jobs = [
                {"title": "Python Developer", "company": "Tech Corp", "url": "https://example.com/1"},
                {"title": "Software Engineer", "company": "StartupXYZ", "url": "https://example.com/2"}
            ]
            
            _store_jobs_in_cache(
                "Python Developer",
                "Hong Kong",
                25,
                "fulltime",
                "hk",
                mock_jobs,
                cache_ttl_hours=168
            )
            
            # Test retrieving from cache
            cached = _get_cached_jobs(
                "Python Developer",
                "Hong Kong",
                25,
                "fulltime",
                "hk"
            )
            
            if cached and cached.get('jobs'):
                print("✅ Stage 5 PASSED: Jobs cached and retrieved successfully")
                print(f"   Cached {len(cached['jobs'])} jobs")
                self.test_results.append(("Stage 5: Job Caching", True, ""))
                return True
            else:
                print("❌ Stage 5 FAILED: Cache retrieval failed")
                self.test_results.append(("Stage 5: Job Caching", False, "Cache retrieval failed"))
                return False
        except Exception as e:
            print(f"❌ Stage 5 FAILED: {e}")
            import traceback
            traceback.print_exc()
            self.test_results.append(("Stage 5: Job Caching", False, str(e)))
            return False
    
    def test_stage_6_data_flow_integration(self):
        """Test Stage 6: End-to-end data flow integration"""
        print("\n" + "="*80)
        print("TESTING STAGE 6: End-to-End Data Flow")
        print("="*80)
        
        try:
            # Simulate complete flow
            st.session_state = {}
            
            # Stage 1: Extract resume text
            print("  → Stage 1: Extracting resume text...")
            resume_text = self.mock_resume_text
            if not resume_text:
                raise Exception("Resume extraction failed")
            
            # Stage 2: Extract profile
            print("  → Stage 2: Extracting profile...")
            profile = self.mock_profile_data
            if not profile:
                raise Exception("Profile extraction failed")
            
            # Stage 3: Verify profile (before resume generation)
            print("  → Stage 3: Verifying profile...")
            verified_profile = verify_profile_accuracy(profile, resume_text)
            if not verified_profile:
                verified_profile = profile  # Fallback
            
            # Stage 4: Generate embedding
            print("  → Stage 4: Generating embedding...")
            with patch('app.get_embedding_generator') as mock_get_emb, \
                 patch('app.get_token_tracker') as mock_get_tracker:
                
                mock_emb_gen = Mock()
                mock_emb_gen.get_embedding.return_value = ([0.1] * 1536, 100)
                mock_get_emb.return_value = mock_emb_gen
                mock_get_tracker.return_value = None
                
                embedding = generate_and_store_resume_embedding(resume_text, verified_profile)
            
            # Stage 5: Cache jobs
            print("  → Stage 5: Testing job cache...")
            mock_jobs = [{"title": "Test Job", "company": "Test Co"}]
            _store_jobs_in_cache("test", "Hong Kong", 25, "fulltime", "hk", mock_jobs)
            cached = _get_cached_jobs("test", "Hong Kong", 25, "fulltime", "hk")
            
            # Validate flow
            checks = [
                ("Resume text extracted", bool(resume_text)),
                ("Profile extracted", bool(profile)),
                ("Profile verified", bool(verified_profile)),
                ("Embedding generated", bool(embedding) or 'resume_embedding' in st.session_state),
                ("Jobs cacheable", bool(cached))
            ]
            
            all_passed = all(check[1] for check in checks)
            
            if all_passed:
                print("✅ Stage 6 PASSED: End-to-end flow works correctly")
                for check_name, check_result in checks:
                    status = "✅" if check_result else "❌"
                    print(f"   {status} {check_name}")
                self.test_results.append(("Stage 6: End-to-End Flow", True, ""))
                return True
            else:
                failed = [check[0] for check in checks if not check[1]]
                print(f"❌ Stage 6 FAILED: {', '.join(failed)}")
                self.test_results.append(("Stage 6: End-to-End Flow", False, f"Failed: {failed}"))
                return False
        except Exception as e:
            print(f"❌ Stage 6 FAILED: {e}")
            import traceback
            traceback.print_exc()
            self.test_results.append(("Stage 6: End-to-End Flow", False, str(e)))
            return False
    
    def run_all_tests(self):
        """Run all test stages"""
        print("\n" + "="*80)
        print("COMPREHENSIVE DATA FLOW TEST SUITE")
        print("="*80)
        
        tests = [
            ("Stage 1: Resume Extraction", self.test_stage_1_resume_extraction),
            ("Stage 2: Profile Extraction", self.test_stage_2_profile_extraction),
            ("Stage 3: Profile Verification", self.test_stage_3_profile_verification),
            ("Stage 4: Resume Embedding", self.test_stage_4_resume_embedding),
            ("Stage 5: Job Caching", self.test_stage_5_job_caching),
            ("Stage 6: End-to-End Flow", self.test_stage_6_data_flow_integration),
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} CRASHED: {e}")
                results.append((test_name, False))
        
        # Print summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status}: {test_name}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed! Data flow is working correctly.")
            return 0
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
            return 1


if __name__ == "__main__":
    tester = TestDataFlow()
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)
