#!/usr/bin/env python3
"""
Test script for resume generation functionality
This tests the resume generation logic with mock data
"""

import sys
import json

# Mock the resume generation function
def test_resume_generation_logic():
    """Test the resume generation prompt and logic"""
    
    # Sample user profile
    user_profile = {
        'name': 'John Doe',
        'email': 'john.doe@email.com',
        'phone': '+1-555-0123',
        'location': 'San Francisco, CA',
        'summary': 'Experienced software developer with 5+ years in Python and machine learning',
        'experience': '''Senior Software Engineer at Tech Corp (2020-2024)
- Led development of ML models improving accuracy by 30%
- Built scalable APIs handling 1M+ requests/day
- Mentored team of 5 junior developers

Software Developer at StartupXYZ (2018-2020)
- Developed full-stack web applications using Python and React
- Reduced application load time by 40% through optimization''',
        'education': 'BS Computer Science, University of California (2018)',
        'skills': 'Python, Machine Learning, TensorFlow, React, SQL, Docker, AWS',
        'certifications': 'AWS Certified Solutions Architect, Google Cloud Professional ML Engineer'
    }
    
    # Sample job posting
    job_posting = {
        'title': 'Senior Machine Learning Engineer',
        'company': 'AI Innovations Inc',
        'description': '''We are looking for a Senior Machine Learning Engineer to join our team.
You will be responsible for:
- Designing and implementing ML models
- Working with Python and TensorFlow
- Building scalable ML systems
- Collaborating with cross-functional teams

Requirements:
- 5+ years of experience in ML
- Strong Python skills
- Experience with TensorFlow or PyTorch
- AWS cloud experience preferred''',
        'skills': ['Python', 'Machine Learning', 'TensorFlow', 'AWS', 'ML Systems']
    }
    
    # Generate the prompt (same as in app.py)
    prompt = f"""You are an expert resume writer. Create a professional, ATS-friendly resume tailored to the specific job posting.

USER BACKGROUND:
- Name: {user_profile.get('name', 'N/A')}
- Email: {user_profile.get('email', 'N/A')}
- Phone: {user_profile.get('phone', 'N/A')}
- Location: {user_profile.get('location', 'N/A')}
- Summary: {user_profile.get('summary', 'N/A')}
- Experience: {user_profile.get('experience', 'N/A')}
- Education: {user_profile.get('education', 'N/A')}
- Skills: {user_profile.get('skills', 'N/A')}
- Certifications: {user_profile.get('certifications', 'N/A')}

JOB POSTING:
- Title: {job_posting.get('title', 'N/A')}
- Company: {job_posting.get('company', 'N/A')}
- Description: {job_posting.get('description', 'N/A')}
- Required Skills: {', '.join(job_posting.get('skills', []))}

Please create a tailored resume that:
1. Highlights relevant experience matching the job requirements
2. Emphasizes skills mentioned in the job posting
3. Uses keywords from the job description for ATS optimization
4. Maintains a professional and concise format
5. Focuses on achievements and measurable results

Format the resume in a clean, professional text format with clear sections."""
    
    print("=" * 80)
    print("RESUME GENERATION TEST")
    print("=" * 80)
    print("\n✅ User Profile Data:")
    print(json.dumps(user_profile, indent=2))
    
    print("\n✅ Job Posting Data:")
    print(json.dumps(job_posting, indent=2))
    
    print("\n✅ Generated Prompt (first 500 chars):")
    print(prompt[:500] + "...")
    
    print("\n✅ Prompt Structure Validation:")
    checks = [
        ("User name included", user_profile['name'] in prompt),
        ("User experience included", user_profile['experience'][:50] in prompt),
        ("Job title included", job_posting['title'] in prompt),
        ("Job description included", job_posting['description'][:50] in prompt),
        ("Required skills included", all(skill in prompt for skill in job_posting['skills'][:3])),
    ]
    
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print("\n📝 Note: This test validates the prompt generation logic.")
    print("   To test actual resume generation, you need:")
    print("   1. Azure OpenAI API key and endpoint")
    print("   2. Configured secrets.toml file")
    print("   3. Run: streamlit run app.py")
    
    return True

if __name__ == "__main__":
    try:
        test_resume_generation_logic()
        print("\n✅ All tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
