import os
import re
import openpyxl

# Configuration Paths
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
PORTS_DIR = os.path.join(REPO_ROOT, "ports")
CSS_FILE = os.path.join(REPO_ROOT, "assets", "css", "port-pages.css")
EXCEL_PATH = r"D:\FalconXoft Ship Chandler\Website Data\Ship_Chandler_SEO_49_Pages_FULL.xlsx"

# Section heading IDs matching Table of Contents and Bissau layout
H2_IDS = [
    'professional-services',
    'provisions',
    'bonded',
    'deck',
    'engine',
    'cabin',
    'safety',
    'electrical',
    'chemicals',
    'welding',
    'spare-parts',
    'publications',
    'tools',
    'technical-support',
    'urgent',
    'vessels',
    'rfq',
    'why-choose',
    None,
    None,
    None,
    None,
]

def render_article_html(desc_text):
    """
    Parses Markdown description into semantic HTML matching Bissau layout
    with feature-grid lists and NO internal article images.
    """
    blocks = [b.strip() for b in desc_text.split('\n\n') if b.strip()]
    lines = []
    h2_index = 0
    
    for b in blocks:
        if b.startswith('# '):
            continue
        elif b.startswith('## '):
            heading_text = b[3:].strip()
            hid = H2_IDS[h2_index] if h2_index < len(H2_IDS) else None
            h2_index += 1
            if hid:
                lines.append(f'          <h2 id="{hid}">{heading_text}</h2>')
            else:
                lines.append(f'          <h2>{heading_text}</h2>')
        elif b.startswith('- '):
            lines.append('          <ul class="feature-grid">')
            for item in b.split('\n'):
                item = item.strip()
                if not item:
                    continue
                val = re.sub(r'^\s*-\s*', '', item)
                lines.append(f'            <li>{val}</li>')
            lines.append('          </ul>')
        else:
            if b.startswith('**') and b.endswith('**'):
                bold_content = b[2:-2].strip()
                lines.append(f'          <p><strong>{bold_content}</strong></p>')
            else:
                clean_p = b.replace('\n', ' ')
                lines.append(f'          <p>{clean_p}</p>')
                
    return '\n'.join(lines)


def build_page_html(page_name, h1, meta_title, meta_desc, full_desc, slug):
    """
    Generates complete HTML for a port page using centralized CSS,
    exact header/footer matching index, hero.jpg image source, and full SEO metadata.
    """
    clean_name = re.sub(r'\b(ship\s*chandlers?|shipchandlers?|ship\s*supply\s*chandler)\b', '', page_name, flags=re.I).strip()
    clean_name = re.sub(r'\s*-\s*.*$', '', clean_name).strip()
    clean_name = re.sub(r'\s+', ' ', clean_name).strip() or page_name

    parts = [page_name.lower()]
    sc_variant = f"ship chandler {clean_name.lower()}"
    if sc_variant != page_name.lower():
        parts.append(sc_variant)
    supply_variant = f"ship supply {clean_name.lower()}"
    if supply_variant not in parts:
        parts.append(supply_variant)
    parts.extend([
        f"port {clean_name.lower()} vessel supply",
        "croatia ship chandler",
        "provisions",
        "marine stores",
        "bonded stores",
        "deck stores",
        "engine stores",
        "vessel supply",
        "marine procurement"
    ])
    new_keywords = ", ".join(parts)
    new_canonical = f"https://shipchandlercroatia.com/ports/{slug}"

    # Style H1 with signature italic accent on "Chandler"
    if re.search(r'\b(Chandlers?)\b', h1, flags=re.I):
        h1_styled = re.sub(r'\b(Chandlers?)\b', r'<em>\1</em>', h1, count=1, flags=re.I)
    else:
        words = h1.split()
        if len(words) > 1:
            h1_styled = " ".join(words[:-1]) + f" <em>{words[-1]}</em>"
        else:
            h1_styled = f"<em>{h1}</em>"

    article_html = render_article_html(full_desc)

    html = f"""<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{meta_title}</title>
  <meta name="description"
    content="{meta_desc}">
  <meta name="keywords"
    content="{new_keywords}">
  <meta name="author" content="SHIP CHANDLER CROATIA CO., LTD">
  <link rel="canonical" href="{new_canonical}">

  <!-- Open Graph Meta Tags -->
  <meta property="og:title" content="{meta_title}">
  <meta property="og:description"
    content="{meta_desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{new_canonical}">
  <meta property="og:site_name" content="Ship Chandler Croatia">

  <!-- Twitter Card Meta Tags -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{meta_title}">
  <meta name="twitter:description"
    content="{meta_desc}">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link
    href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap"
    rel="stylesheet">

  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <!-- Favicon & App Icons -->
  <link rel="icon" type="image/png" href="../favicon.png">
  <link rel="shortcut icon" href="../favicon.ico">
  <link rel="apple-touch-icon" href="../assets/imgs/favicon.png">

  <!-- Centralized Port Pages CSS -->
  <link rel="stylesheet" href="../assets/css/port-pages.css">
</head>

<body>

  <!-- NAVBAR -->
  <header class="site-header" id="site-header">
    <div class="header-inner">
      <a class="logo" href="../index.html">
        <img src="../assets/imgs/logo.png" alt="Ship Chandler Croatia Logo">
        <span class="logo-text">
          <strong>ShipChandler</strong>
          <span>Croatia</span>
        </span>
      </a>

      <button class="nav-toggle" type="button" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>

      <nav class="primary-nav" id="primary-nav">
        <ul class="nav-list">
          <li class="nav-item"><a class="nav-link" href="../index.html">Home</a></li>
          <li class="nav-item"><a class="nav-link" href="../about.html">About</a></li>

          <li class="nav-item has-dropdown">
            <a class="nav-link" href="../services.html">Services <span class="nav-arrow"><svg viewBox="0 0 24 24"
                  width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg></span></a>
            <div class="dropdown-menu">
              <a href="../services.html#provisions">Food Provisions Supply</a>
              <a href="../services.html#bonded">Bonded Stores</a>
              <a href="../services.html#deck">Deck Stores</a>
              <a href="../services.html#engine">Engine Stores</a>
              <a href="../services.html#cabin">Cabin & Galley</a>
              <a href="../services.html#safety">Safety & PPE</a>
              <a href="../services.html#electrical">Electrical Stores</a>
              <a href="../services.html#chemicals">Marine Chemicals</a>
              <a href="../services.html#welding">Welding Equipment</a>
              <a href="../services.html#spare-parts">Spare Parts</a>
              <a href="../services.html#publications">Nautical Charts</a>
              <a href="../services.html#tools">Tools & Hardware</a>
              <a href="../services.html#urgent">Urgent Supply</a>
            </div>
          </li>

          <li class="nav-item has-mega active">
            <a class="nav-link" href="javascript:void(0)">Ports <span class="nav-arrow"><svg viewBox="0 0 24 24"
                  width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg></span></a>
            <div class="mega-menu">
              <div class="mega-header">
                <div class="mega-header-title">Global Port Network</div>
                <div class="mega-search">
                  <i class="fas fa-search" style="color:var(--gray-500);"></i>
                  <input type="text" id="mega-port-search" placeholder="Search 49 ports...">
                </div>
              </div>
              <div class="mega-grid" id="mega-port-list"></div>
            </div>
          </li>

          <li class="nav-item"><a class="nav-link" href="../contact.html">Contact</a></li>
        </ul>
        <a class="btn btn-red" style="padding: 10px 24px; font-size: 0.82rem;" href="../request-quote.html">Get
          Quote</a>
      </nav>
    </div>
  </header>

  <main>
    <!-- SUBPAGE HERO -->
    <section class="subpage-hero">
      <img src="../assets/imgs/hero.jpg" alt="{h1}" class="subpage-hero-bg">
      <div class="subpage-hero-overlay"></div>
      <div class="container subpage-hero-content">
        <ul class="breadcrumb reveal">
          <li><a href="../index.html">Home</a></li>
          <li><span>/</span></li>
          <li>{page_name}</li>
        </ul>
        <h1 class="subpage-hero-title reveal reveal-delay-1">{h1_styled}</h1>
        <p class="subpage-hero-desc reveal reveal-delay-2">{meta_desc}</p>
      </div>
    </section>

    <!-- ARTICLE CONTENT SECTION -->
    <section class="article-section">
      <div class="container">

        <!-- Modern Quick Navigation (Sticky Bar) -->
        <div class="quick-nav-wrapper reveal">
          <div class="quick-nav">
            <a href="#professional-services">Professional Ship Supply</a>
            <a href="#provisions">Provisions</a>
            <a href="#bonded">Bonded Stores</a>
            <a href="#deck">Deck Stores</a>
            <a href="#engine">Engine Stores</a>
            <a href="#cabin">Cabin & Galley</a>
            <a href="#safety">Safety Equipment</a>
            <a href="#electrical">Electrical Stores</a>
            <a href="#chemicals">Marine Chemicals</a>
            <a href="#welding">Welding Equipment</a>
            <a href="#spare-parts">Spare Parts</a>
            <a href="#publications">Nautical Charts</a>
            <a href="#tools">Tools & Hardware</a>
            <a href="#technical-support">Technical Support</a>
            <a href="#urgent">Urgent Supply</a>
            <a href="#vessels">Vessels Supported</a>
            <a href="#rfq">How to Send RFQ</a>
            <a href="#why-choose">Why Choose Us</a>
          </div>
        </div>

        <!-- Main Article Content -->
        <article class="article-content" style="transition-delay: 0.1s;">
{article_html}
        </article>
      </div>
    </section>
  </main>

  <!-- FOOTER -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <a class="logo" href="../index.html">
            <img src="../assets/imgs/logo.png" alt="Logo">
            <span class="logo-text">
              <strong>ShipChandler</strong>
              <span>Croatia</span>
            </span>
          </a>
          <p>SHIP CHANDLER CROATIA CO., LTD is a licensed marine supplier providing food provisions, food stores, bond
            store supply, drinks, snacks, and emergency vessel supply services across all major Croatian ports.</p>
        </div>

        <div class="footer-col">
          <h4>Quick Links</h4>
          <ul class="footer-links">
            <li><a href="../index.html">Home</a></li>
            <li><a href="../about.html">About Us</a></li>
            <li><a href="../services.html">Services</a></li>
            <li><a href="../contact.html">Contact</a></li>
            <li><a href="../request-quote.html">Request a Quote</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Services</h4>
          <ul class="footer-links">
            <li><a href="../services.html#provisions">Provisions Supply</a></li>
            <li><a href="../services.html#bonded">Bonded Stores</a></li>
            <li><a href="../services.html#deck">Deck Stores</a></li>
            <li><a href="../services.html#engine">Engine Stores</a></li>
            <li><a href="../services.html#urgent">Urgent Supply</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Contact</h4>
          <ul class="footer-contact">
            <li><i class="fas fa-map-marker-alt"></i> Port of Rijeka, Riva 1, 51000 Rijeka, Croatia</li>
            <li><i class="fas fa-envelope"></i> <a href="mailto:sales@shipchandlercroatia.com"
                style="color:inherit;">sales@shipchandlercroatia.com</a></li>
            <li><i class="fas fa-user-tie"></i> Ivan Kovačević</li>
            <li style="margin-top: 10px;">
              <a class="footer-whatsapp-btn" href="https://wa.me/6590190005" target="_blank" rel="noopener noreferrer">
                <i class="fab fa-whatsapp"></i> WhatsApp: (+65-9019-0005)
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <div>&copy; 2026 SHIP CHANDLER CROATIA CO., LTD. All rights reserved.</div>
      </div>
    </div>
  </footer>

  <!-- FLOATING WHATSAPP -->
  <a href="https://wa.me/6590190005" class="whatsapp-float" target="_blank" rel="noopener noreferrer"
    aria-label="WhatsApp Contact +65-9019-0005">
    <i class="fab fa-whatsapp"></i>
  </a>

  <script>
    // --- Global Port List (49 Ports) ---
    const ports = [
      "Ship Chandler Dar Es Salaam", "Ship Chandler Apapa", "Ship Chandler Onne Port Nigeria", "San Pedro Ship Supply Chandler",
      "Ship Chandler Abidjan", "Ship Chandler Freetown", "Monrovia Ship Chandler", "Ship Chandler Maputo", "Ship Chandler Matadi",
      "Ship Chandler Beira", "Ship Chandler Angola", "Ship Chandler Lobito", "ShipChandler Lome", "Shipchandler Lome",
      "Ivory Coast Ship Chandler", "Nouadhibou Ship Chandler", "Ship Chandler Luanda", "Ship Chandler Cape Verde",
      "Ship Chandler Gabon", "Ship Chandler Namibia", "Walvis Bay Ship Chandler", "Ship Chandler Gentil Port - Gabon",
      "Ship Chandler Takoradi", "Ship Chandler Congo", "Shipchandler Lagos", "Ship Chandler Port Ambon",
      "Shipchandler Pointe Noire", "Ship Chandler Djibouti", "Ship Chandler Cabinda", "Ship Chandler Tema",
      "Ship Chandler Mindelo", "Ship Chandler Casablanca", "Ship Chandler Safi Port Morocco", "Ship Chandler Kamsar",
      "Ship Chandler Soyo", "Dakar Ship Chandler", "Ship Chandler Senegal", "Ship Chandler Dakar", "Bissau Ship Chandler - Guinea",
      "Conakry Ship Chandler", "Ship Chandler Cotonou", "Douala Ship Chandler", "Liberia Ship Chandler", "Namibia Ship Chandler",
      "Ship Chandler Dakar", "Ship Chandler Mombasa", "Ship Chandlers Saldanha Bay", "Ship Chandler Owendo", "Ship Chandlers Richards Bay"
    ];

    // Populate Mega Menu
    const megaList = document.getElementById('mega-port-list');
    if (megaList) {{
      const fourth = Math.ceil(ports.length / 4);
      const col1 = ports.slice(0, fourth);
      const col2 = ports.slice(fourth, fourth * 2);
      const col3 = ports.slice(fourth * 2, fourth * 3);
      const col4 = ports.slice(fourth * 3);

      function createPortGroup(title, items) {{
        if (items.length === 0) return document.createElement('div');
        const group = document.createElement('div');
        group.className = 'mega-group';
        group.innerHTML = `<h4>${{title}}</h4>`;
        items.forEach(port => {{
          const a = document.createElement('a');
          a.href = `../ports/${{port.toLowerCase().replace(/[^a-z0-9]+/g, '-')}}.html`;
          a.textContent = port;
          group.appendChild(a);
        }});
        return group;
      }}

      megaList.appendChild(createPortGroup('African Ports (A-D)', col1));
      megaList.appendChild(createPortGroup('African Ports (E-M)', col2));
      megaList.appendChild(createPortGroup('African Ports (N-S)', col3));
      megaList.appendChild(createPortGroup('African Ports (T-Z)', col4));

      // Mega Menu Search
      const searchInput = document.getElementById('mega-port-search');
      if (searchInput) {{
        searchInput.addEventListener('input', function (e) {{
          const query = e.target.value.toLowerCase();
          const allLinks = megaList.querySelectorAll('a');
          const groups = megaList.querySelectorAll('.mega-group');

          allLinks.forEach(link => {{
            const text = link.textContent.toLowerCase();
            link.style.display = text.includes(query) ? 'block' : 'none';
          }});

          groups.forEach(group => {{
            const hasVisible = Array.from(group.querySelectorAll('a')).some(a => a.style.display !== 'none');
            group.style.display = hasVisible ? 'block' : 'none';
          }});
        }});
      }}
    }}

    document.addEventListener('DOMContentLoaded', function () {{

      // --- Sticky Header Effect ---
      const header = document.querySelector('.site-header');
      window.addEventListener('scroll', () => {{
        if (window.scrollY > 20) {{
          header.classList.add('scrolled');
        }} else {{
          header.classList.remove('scrolled');
        }}
      }});

      // --- Mobile Nav Toggle ---
      const navToggle = document.querySelector('.nav-toggle');
      const primaryNav = document.querySelector('.primary-nav');

      navToggle.addEventListener('click', function () {{
        primaryNav.classList.toggle('open');
        this.classList.toggle('open');
      }});

      // --- Mobile Dropdown Toggles ---
      const dropdownItems = document.querySelectorAll('.nav-item.has-dropdown, .nav-item.has-mega');
      dropdownItems.forEach(item => {{
        const link = item.querySelector('.nav-link');
        link.addEventListener('click', function (e) {{
          if (window.innerWidth <= 1024) {{
            e.preventDefault();
            item.classList.toggle('open');
          }}
        }});
      }});

      // --- Scroll Reveal Animation ---
      const revealElements = document.querySelectorAll('.reveal');
      const revealObserver = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
          if (entry.isIntersecting) {{
            entry.target.classList.add('active');
            revealObserver.unobserve(entry.target);
          }}
        }});
      }}, {{
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
      }});

      revealElements.forEach(el => revealObserver.observe(el));

      // --- Quick Nav Active State Tracking ---
      const quickNavLinks = document.querySelectorAll('.quick-nav a');
      const headings = document.querySelectorAll('.article-content h2');

      window.addEventListener('scroll', () => {{
        let current = '';

        headings.forEach(heading => {{
          const headingTop = heading.offsetTop;
          if (scrollY >= headingTop - 200) {{
            current = heading.getAttribute('id');
          }}
        }});

        quickNavLinks.forEach(link => {{
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${{current}}`) {{
            link.classList.add('active');
          }}
        }});
      }});

    }});
  </script>
</body>

</html>
"""
    return html


def main():
    print(f"Reading Excel data from: {EXCEL_PATH}")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    sheet = wb['SEO Pages']
    
    rows = list(sheet.iter_rows(values_only=True))[1:]
    print(f"Found {len(rows)} port rows in Excel.")
    
    generated_count = 0
    generated_files = set()
    
    for row in rows:
        num, page_name, h1, meta_title, meta_desc, full_desc = row[:6]
        if not page_name:
            continue
            
        slug = re.sub(r'[^a-z0-9]+', '-', str(page_name).lower()).strip('-') + '.html'
        out_path = os.path.join(PORTS_DIR, slug)
        
        html_content = build_page_html(
            page_name=str(page_name).strip(),
            h1=str(h1).strip(),
            meta_title=str(meta_title).strip(),
            meta_desc=str(meta_desc).strip(),
            full_desc=str(full_desc).strip(),
            slug=slug
        )
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        generated_count += 1
        generated_files.add(slug)
        print(f"[{num:02d}/49] Generated: {slug} ({page_name})")
        
    print("\n" + "="*60)
    print(f"SUCCESS: Processed {generated_count} rows across {len(generated_files)} unique port files.")
    print(f"Centralized CSS: assets/css/port-pages.css")
    print(f"Image used in each page: ../assets/imgs/hero.jpg")
    print("="*60)

if __name__ == "__main__":
    main()
