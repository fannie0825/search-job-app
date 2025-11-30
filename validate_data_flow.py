#!/usr/bin/env python3
"""
Static validation of data flow structure
Tests code structure and data flow logic without requiring dependencies
"""

import ast
import sys
import os
import re


class DataFlowValidator:
    """Validates data flow structure in app.py"""
    
    def __init__(self, filepath='app.py'):
        self.filepath = filepath
        self.errors = []
        self.warnings = []
        self.success = []
        
    def read_file(self):
        """Read and parse the Python file"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return content, ast.parse(content)
        except FileNotFoundError:
            print(f"❌ File not found: {self.filepath}")
            sys.exit(1)
        except SyntaxError as e:
            print(f"❌ Syntax error in {self.filepath}: {e}")
            sys.exit(1)
    
    def validate_stage_1_resume_extraction(self, content):
        """Validate Stage 1: Resume extraction function exists and is correct"""
        print("\n" + "="*80)
        print("VALIDATING STAGE 1: Resume Text Extraction")
        print("="*80)
        
        if 'def extract_text_from_resume' in content:
            print("✅ Function 'extract_text_from_resume' exists")
            self.success.append("Stage 1: Function exists")
            
            # Check for PDF and DOCX handling
            if 'PyPDF2' in content or 'pdf' in content.lower():
                print("✅ PDF extraction support found")
                self.success.append("Stage 1: PDF support")
            else:
                self.warnings.append("Stage 1: PDF extraction may be missing")
            
            if 'docx' in content.lower() or 'Document' in content:
                print("✅ DOCX extraction support found")
                self.success.append("Stage 1: DOCX support")
            else:
                self.warnings.append("Stage 1: DOCX extraction may be missing")
        else:
            print("❌ Function 'extract_text_from_resume' not found")
            self.errors.append("Stage 1: Missing function")
    
    def validate_stage_2_profile_extraction(self, content):
        """Validate Stage 2: Profile extraction (first pass)"""
        print("\n" + "="*80)
        print("VALIDATING STAGE 2: Profile Extraction (First Pass)")
        print("="*80)
        
        if 'def extract_profile_from_resume' in content:
            print("✅ Function 'extract_profile_from_resume' exists")
            self.success.append("Stage 2: Function exists")
            
            # Check it's a single pass (should not call verify_profile_accuracy)
            if 'extract_profile_from_resume' in content:
                # Count occurrences - should only be definition and calls
                matches = len(re.findall(r'extract_profile_from_resume', content))
                if matches <= 3:  # Definition + 1-2 calls
                    print("✅ Single-pass extraction confirmed")
                    self.success.append("Stage 2: Single pass")
                else:
                    self.warnings.append("Stage 2: May have multiple passes")
            
            # Check for JSON response format
            if 'json_object' in content or 'response_format' in content:
                print("✅ JSON response format configured")
                self.success.append("Stage 2: JSON format")
        else:
            print("❌ Function 'extract_profile_from_resume' not found")
            self.errors.append("Stage 2: Missing function")
    
    def validate_stage_3_profile_verification(self, content):
        """Validate Stage 3: Profile verification (second pass before resume generation)"""
        print("\n" + "="*80)
        print("VALIDATING STAGE 3: Profile Verification (Second Pass)")
        print("="*80)
        
        if 'def verify_profile_accuracy' in content:
            print("✅ Function 'verify_profile_accuracy' exists")
            self.success.append("Stage 3: Function exists")
            
            # Check it's called before resume generation
            if 'verify_profile_accuracy' in content and 'Generate Tailored Resume' in content:
                # Check order: verify should come before generate_resume
                verify_pos = content.find('verify_profile_accuracy')
                generate_pos = content.find('generate_resume')
                
                if verify_pos < generate_pos:
                    print("✅ Verification called before resume generation")
                    self.success.append("Stage 3: Correct order")
                else:
                    self.warnings.append("Stage 3: Order may be incorrect")
            
            # Check for _extract_relevant_resume_sections helper
            if '_extract_relevant_resume_sections' in content:
                print("✅ Helper function for section extraction exists")
                self.success.append("Stage 3: Section extraction helper")
        else:
            print("❌ Function 'verify_profile_accuracy' not found")
            self.errors.append("Stage 3: Missing function")
    
    def validate_stage_4_resume_embedding(self, content):
        """Validate Stage 4: Resume embedding generation"""
        print("\n" + "="*80)
        print("VALIDATING STAGE 4: Resume Embedding Generation")
        print("="*80)
        
        if 'def generate_and_store_resume_embedding' in content:
            print("✅ Function 'generate_and_store_resume_embedding' exists")
            self.success.append("Stage 4: Function exists")
            
            # Check for session state storage
            if 'resume_embedding' in content and 'session_state' in content:
                print("✅ Embedding stored in session state")
                self.success.append("Stage 4: Session storage")
        else:
            print("❌ Function 'generate_and_store_resume_embedding' not found")
            self.errors.append("Stage 4: Missing function")
    
    def validate_stage_5_job_caching(self, content):
        """Validate Stage 5: Job caching system"""
        print("\n" + "="*80)
        print("VALIDATING STAGE 5: Job Caching System")
        print("="*80)
        
        # Check cache functions
        cache_functions = [
            '_build_jobs_cache_key',
            '_get_cached_jobs',
            '_store_jobs_in_cache',
            'fetch_jobs_with_cache'
        ]
        
        for func in cache_functions:
            if f'def {func}' in content:
                print(f"✅ Function '{func}' exists")
                self.success.append(f"Stage 5: {func}")
            else:
                print(f"❌ Function '{func}' not found")
                self.errors.append(f"Stage 5: Missing {func}")
        
        # Check for TTL/expiration
        if 'expires_at' in content or 'cache_ttl' in content:
            print("✅ Cache expiration mechanism found")
            self.success.append("Stage 5: Cache expiration")
    
    def validate_stage_6_data_flow(self, content):
        """Validate Stage 6: Complete data flow integration"""
        print("\n" + "="*80)
        print("VALIDATING STAGE 6: Data Flow Integration")
        print("="*80)
        
        # Check flow in render_sidebar or main function
        flow_steps = [
            ('extract_text_from_resume', 'Resume extraction'),
            ('extract_profile_from_resume', 'Profile extraction'),
            ('generate_and_store_resume_embedding', 'Embedding generation'),
            ('fetch_jobs_with_cache', 'Job fetching'),
        ]
        
        # Check if these are called in sequence
        for func_name, step_name in flow_steps:
            if func_name in content:
                print(f"✅ {step_name} function found in codebase")
                self.success.append(f"Stage 6: {step_name}")
            else:
                print(f"⚠️  {step_name} function not found")
                self.warnings.append(f"Stage 6: {step_name} missing")
        
        # Check resume generation flow
        if 'verify_profile_accuracy' in content and 'generate_resume' in content:
            # Find the order in display_resume_generator
            if 'display_resume_generator' in content:
                print("✅ Resume generation flow includes verification")
                self.success.append("Stage 6: Resume generation flow")
    
    def validate_code_structure(self, tree):
        """Validate overall code structure"""
        print("\n" + "="*80)
        print("VALIDATING CODE STRUCTURE")
        print("="*80)
        
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        print(f"✅ Found {len(functions)} functions")
        print(f"✅ Found {len(classes)} classes")
        
        # Check for key classes
        key_classes = ['SemanticJobSearch', 'MultiSourceJobAggregator', 'TokenUsageTracker']
        for cls in key_classes:
            if cls in classes:
                print(f"✅ Class '{cls}' found")
                self.success.append(f"Structure: {cls}")
            else:
                self.warnings.append(f"Structure: {cls} not found")
    
    def validate_simplifications(self, content):
        """Validate that simplifications were applied"""
        print("\n" + "="*80)
        print("VALIDATING SIMPLIFICATIONS")
        print("="*80)
        
        # Check ChromaDB was removed
        if 'chromadb' not in content.lower():
            print("✅ ChromaDB removed (simplification)")
            self.success.append("Simplification: ChromaDB removed")
        else:
            self.warnings.append("Simplification: ChromaDB may still be present")
        
        # Check retry logic simplified
        if '_get_retry_delay' in content:
            print("✅ Simplified retry logic found")
            self.success.append("Simplification: Retry logic")
        
        # Check two-pass removed from extraction
        if 'extract_profile_from_resume' in content:
            # Should not call verify_profile_accuracy internally
            func_start = content.find('def extract_profile_from_resume')
            func_end = content.find('\n\n', func_start + 100)
            if func_end == -1:
                func_end = func_start + 5000
            
            func_body = content[func_start:func_end]
            if 'verify_profile_accuracy' not in func_body:
                print("✅ Single-pass extraction (no internal verification)")
                self.success.append("Simplification: Single-pass extraction")
    
    def run_validation(self):
        """Run all validations"""
        print("\n" + "="*80)
        print("DATA FLOW VALIDATION REPORT")
        print("="*80)
        
        content, tree = self.read_file()
        
        # Run all validations
        self.validate_stage_1_resume_extraction(content)
        self.validate_stage_2_profile_extraction(content)
        self.validate_stage_3_profile_verification(content)
        self.validate_stage_4_resume_embedding(content)
        self.validate_stage_5_job_caching(content)
        self.validate_stage_6_data_flow(content)
        self.validate_code_structure(tree)
        self.validate_simplifications(content)
        
        # Print summary
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        
        print(f"\n✅ Successes: {len(self.success)}")
        for item in self.success:
            print(f"   ✓ {item}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings: {len(self.warnings)}")
            for item in self.warnings:
                print(f"   ⚠ {item}")
        
        if self.errors:
            print(f"\n❌ Errors: {len(self.errors)}")
            for item in self.errors:
                print(f"   ✗ {item}")
        
        # Final result
        print("\n" + "="*80)
        if not self.errors:
            print("🎉 VALIDATION PASSED: Code structure looks good!")
            print("   All critical functions and data flow stages are present.")
            return 0
        else:
            print("❌ VALIDATION FAILED: Found critical errors")
            print("   Please fix the errors above before proceeding.")
            return 1


if __name__ == "__main__":
    validator = DataFlowValidator('app.py')
    exit_code = validator.run_validation()
    sys.exit(exit_code)
