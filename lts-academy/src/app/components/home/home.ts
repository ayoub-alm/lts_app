import {
  Component,
  AfterViewInit,
  OnDestroy,
  ElementRef,
  Inject,
  PLATFORM_ID
} from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { FormationService } from '../../services/formation.service';
import { SeoService } from '../../services/seo.service';
import { LanguageDetectorComponent } from '../language-detector/language-detector';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    LanguageDetectorComponent
  ],
  templateUrl: './home.html',
  styleUrls: ['./home.scss']
})
export class Home implements AfterViewInit, OnDestroy {
  topFormations;
  private animationFrames: number[] = [];

  constructor(
    private formationService: FormationService,
    private el: ElementRef,
    private seoService: SeoService,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    this.topFormations = this.formationService.getFormations().slice(0, 6);

    this.seoService.updateMetaTags({
      title: 'Accueil - LTS Academy',
      description:
        'Découvrez LTS Academy, votre partenaire pour la formation professionnelle et les services digitaux au Maroc. Formations diplômantes, développement web et solutions IT.',
      image: '/assets/lts.png'
    });
    this.seoService.setCanonicalURL();
    this.seoService.setJsonLd({
      '@context': 'https://schema.org',
      '@type': 'EducationalOrganization',
      name: 'LTS Academy',
      url: 'https://ltsacademy.ma',
      logo: 'https://ltsacademy.ma/assets/logo_new.jpeg',
      sameAs: [
        'https://www.facebook.com/ltsacademy',
        'https://www.linkedin.com/company/lts-academy'
      ],
      address: {
        '@type': 'PostalAddress',
        streetAddress: 'Centre Ville',
        addressLocality: 'Berrechid',
        addressCountry: 'MA'
      },
      contactPoint: {
        '@type': 'ContactPoint',
        telephone: '+212-660-356877',
        contactType: 'customer service'
      }
    });
  }

  ngAfterViewInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      setTimeout(() => this.initAnimations(), 100);
    }
  }

  ngOnDestroy(): void {
    this.animationFrames.forEach(id => cancelAnimationFrame(id));
  }

  private initAnimations(): void {
    // Simple CSS-based reveal animation for scroll elements
    const revealElements = this.el.nativeElement.querySelectorAll('.reveal');
    if (typeof IntersectionObserver === 'undefined') return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            (entry.target as HTMLElement).classList.add('revealed');
          }
        });
      },
      { threshold: 0.15 }
    );

    revealElements.forEach((el: Element) => observer.observe(el));
  }
}
