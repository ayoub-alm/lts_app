import { Injectable, Inject } from '@angular/core';
import { Meta, Title } from '@angular/platform-browser';
import { DOCUMENT } from '@angular/common';

export interface SeoConfig {
  title?: string;
  description?: string;
  image?: string;
  url?: string;
}

@Injectable({
  providedIn: 'root'
})
export class SeoService {
  constructor(
    private meta: Meta,
    private title: Title,
    @Inject(DOCUMENT) private document: Document
  ) {}

  updateMetaTags(config: SeoConfig): void {
    if (config.title) {
      this.title.setTitle(config.title);
      this.meta.updateTag({ property: 'og:title', content: config.title });
    }
    if (config.description) {
      this.meta.updateTag({ name: 'description', content: config.description });
      this.meta.updateTag({ property: 'og:description', content: config.description });
    }
    if (config.image) {
      this.meta.updateTag({ property: 'og:image', content: config.image });
    }
    if (config.url) {
      this.meta.updateTag({ property: 'og:url', content: config.url });
    }
  }

  setCanonicalURL(url?: string): void {
    const existingLink = this.document.querySelector('link[rel="canonical"]');
    const link: HTMLLinkElement = existingLink as HTMLLinkElement || this.document.createElement('link');
    link.setAttribute('rel', 'canonical');
    link.setAttribute('href', url || this.document.URL);
    if (!existingLink) {
      this.document.head.appendChild(link);
    }
  }

  setJsonLd(data: object): void {
    const existing = this.document.querySelector('script[type="application/ld+json"]');
    if (existing) {
      existing.textContent = JSON.stringify(data);
    } else {
      const script = this.document.createElement('script');
      script.type = 'application/ld+json';
      script.text = JSON.stringify(data);
      this.document.head.appendChild(script);
    }
  }
}
