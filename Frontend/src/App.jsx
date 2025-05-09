import { useState } from 'react';
import './index.css';

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitting:', { email, password });
  };

  return (
    <div className="app">
      {/* Navigation */}
      <nav className="navbar">
        <div className="nav-container">
          <div className="logo">Novaspire</div>
          <div className="nav-links">
            <a href="#features">Features</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#testimonials">Success Stories</a>
            <button className="nav-cta">Get Started</button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-container">
          <div className="hero-content">
            <h1>Transform Your Career with AI-Powered Resume Analysis</h1>
            <p className="hero-subtitle">The most advanced resume optimization platform trusted by professionals worldwide</p>
            
            <form onSubmit={handleSubmit} className="hero-form">
              <div className="form-group">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Your professional email"
                  required
                />
              </div>
              <div className="form-group">
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.value)}
                  placeholder="Create secure password"
                  required
                />
              </div>
              <button type="submit" className="cta-button">
                <span>Start Free Analysis</span>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </button>
            </form>
            
            <div className="trust-badges">
              <div className="badge">Forbes Tech Council</div>
              <div className="badge">WSJ Recommended</div>
            </div>
          </div>
          <div className="hero-image">
            <img src="https://images.unsplash.com/photo-1521791136064-7986c2920216?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80" alt="Professional analyzing resume" />
            <div className="image-overlay"></div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats">
        <div className="stats-container">
          <div className="stat-item">
            <h3>98%</h3>
            <p>Interview Rate Increase</p>
          </div>
          <div className="stat-item">
            <h3>10,000+</h3>
            <p>Professionals Hired</p>
          </div>
          <div className="stat-item">
            <h3>4.9/5</h3>
            <p>User Satisfaction</p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features">
        <div className="section-header">
          <h2>Enterprise-Grade Resume Optimization</h2>
          <p className="section-subtitle">Powered by cutting-edge AI technology</p>
        </div>
        
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#4B5320" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <h3>ATS Compliance Scan</h3>
            <p>Ensure your resume passes through applicant tracking systems with our proprietary scanning technology.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 6V12L16 14M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="#4B5320" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <h3>Real-Time Optimization</h3>
            <p>Get instant suggestions to improve your resume's impact and readability.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 21L12 16L5 21V5C5 4.46957 5.21071 3.96086 5.58579 3.58579C5.96086 3.21071 6.46957 3 7 3H17C17.5304 3 18.0391 3.21071 18.4142 3.58579C18.7893 3.96086 19 4.46957 19 5V21Z" stroke="#4B5320" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <h3>Industry-Specific Templates</h3>
            <p>Choose from professionally designed templates tailored to your industry.</p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="how-it-works">
        <div className="section-header">
          <h2>How Novaspire Works</h2>
          <p className="section-subtitle">Three simple steps to resume perfection</p>
        </div>
        
        <div className="steps-container">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Upload Your Resume</h3>
            <p>Securely upload your existing resume in any format (PDF, DOCX, TXT).</p>
          </div>
          
          <div className="step">
            <div className="step-number">2</div>
            <h3>AI Analysis</h3>
            <p>Our algorithms scan and evaluate your resume against industry standards.</p>
          </div>
          
          <div className="step">
            <div className="step-number">3</div>
            <h3>Get Optimized</h3>
            <p>Receive actionable insights and a perfected resume ready for applications.</p>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="testimonials">
        <div className="section-header">
          <h2>Success Stories</h2>
          <p className="section-subtitle">Trusted by professionals at top companies</p>
        </div>
        
        <div className="testimonials-grid">
          <div className="testimonial-card">
            <div className="testimonial-content">
              <p>"Novaspire helped me land interviews at Google, Amazon, and Microsoft within two weeks of using their service."</p>
            </div>
            <div className="testimonial-author">
              <img src="https://randomuser.me/api/portraits/women/44.jpg" alt="Sarah J." />
              <div>
                <h4>Sarah Johnson</h4>
                <p>Senior Software Engineer</p>
              </div>
            </div>
          </div>
          
          <div className="testimonial-card">
            <div className="testimonial-content">
              <p>"After using Novaspire, my response rate from applications increased by 300%. Worth every penny."</p>
            </div>
            <div className="testimonial-author">
              <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="Michael T." />
              <div>
                <h4>Michael Thompson</h4>
                <p>Marketing Director</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-container">
          <h2>Ready to Transform Your Job Search?</h2>
          <p>Join thousands of professionals who've accelerated their careers with Novaspire.</p>
          <button className="cta-button secondary">
            <span>Start Free Analysis</span>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 12H19M19 12L12 5M19 12L12 19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-container">
          <div className="footer-logo">Novaspire</div>
          
          <div className="footer-links">
            <div className="link-group">
              <h4>Product</h4>
              <a href="#">Features</a>
              <a href="#">Pricing</a>
              <a href="#">Examples</a>
            </div>
            
            <div className="link-group">
              <h4>Company</h4>
              <a href="#">About</a>
              <a href="#">Careers</a>
              <a href="#">Press</a>
            </div>
            
            <div className="link-group">
              <h4>Resources</h4>
              <a href="#">Blog</a>
              <a href="#">Help Center</a>
              <a href="#">Contact</a>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>© 2025 Novaspire. All rights reserved.</p>
          <div className="legal-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;