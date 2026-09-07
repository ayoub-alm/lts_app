import { Component, HostListener, Inject, PLATFORM_ID, signal } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { RouterModule, RouterLink, RouterLinkActive, Router } from '@angular/router';
import { FormationService } from '../../services/formation.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule, RouterLink, RouterLinkActive],
  templateUrl: './header.html',
  styleUrls: ['./header.scss']
})
export class HeaderComponent {
  scrolled     = signal(false);
  mobileOpen   = signal(false);
  dropdownOpen = signal(false);

  // Icon map for each formation id
  private readonly iconMap: Record<string, string> = {
    'marketing':        'bi-megaphone',
    'rh':               'bi-people',
    'logistique':       'bi-truck',
    'web-development':  'bi-code-slash',
    'big-data':         'bi-cpu',
    'design':           'bi-palette',
    'finance':          'bi-cash-stack',
    'langues':          'bi-translate',
    'systemes-reseaux': 'bi-hdd-network',
    'mecanique':        'bi-wrench-adjustable',
    'paramedical':      'bi-heart-pulse',
    'qhse':             'bi-shield-check',
  };

  formations: { label: string; path: string; icon: string }[] = [];

  constructor(
    private router: Router,
    private formationService: FormationService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    // Dynamically build nav dropdown from the service data
    this.formations = this.formationService.getFormations().map(f => ({
      label: f.title,
      path: `/formations/${f.id}`,
      icon: this.iconMap[f.id] || 'bi-book',
    }));
  }

  @HostListener('window:scroll')
  onScroll(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.scrolled.set(window.scrollY > 20);
    }
  }

  @HostListener('document:click', ['$event'])
  onDocClick(e: MouseEvent): void {
    const target = e.target as HTMLElement;
    if (!target.closest('.nav-dropdown-wrap')) {
      this.dropdownOpen.set(false);
    }
  }

  toggleDropdown(e: MouseEvent): void {
    e.stopPropagation();
    this.dropdownOpen.update(v => !v);
  }

  openDropdown(): void {
    this.dropdownOpen.set(true);
  }

  closeDropdown(): void {
    this.dropdownOpen.set(false);
  }

  toggleMobile(): void {
    this.mobileOpen.update(v => !v);
  }

  closeMobile(): void {
    this.mobileOpen.set(false);
  }

  navigateToHome(e?: Event): void {
    if (e) e.preventDefault();
    this.closeDropdown();
    this.closeMobile();
    const currentUrl = this.router.url.split('#')[0];
    if (currentUrl === '/' || currentUrl === '') {
      if (isPlatformBrowser(this.platformId)) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    } else {
      this.router.navigate(['/']).then(() => {
        if (isPlatformBrowser(this.platformId)) {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      });
    }
  }

  navigateToContact(e?: Event): void {
    if (e) e.preventDefault();
    this.closeDropdown();
    this.closeMobile();

    if (isPlatformBrowser(this.platformId)) {
      const currentUrl = this.router.url.split('#')[0];
      if (currentUrl === '/' || currentUrl === '') {
        const contactEl = document.getElementById('contact');
        if (contactEl) {
          contactEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
          return;
        }
      }

      this.router.navigate(['/'], { fragment: 'contact' }).then(() => {
        setTimeout(() => {
          const contactEl = document.getElementById('contact');
          if (contactEl) {
            contactEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 150);
      });
    } else {
      this.router.navigate(['/'], { fragment: 'contact' });
    }
  }
}
