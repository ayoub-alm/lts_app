import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { AiService, LanguageDetectResponse } from '../../services/ai.service';

interface Language {
  code: string;
  label: string;
  flag: string;
  placeholder: string;
}

@Component({
  selector: 'app-language-detector',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatIconModule,
    MatButtonModule,
    MatSelectModule,
    MatFormFieldModule
  ],
  templateUrl: './language-detector.html',
  styleUrls: ['./language-detector.scss']
})
export class LanguageDetectorComponent {
  languages: Language[] = [
    {
      code: 'Français',
      label: 'Français',
      flag: '🇫🇷',
      placeholder: 'Écrivez 3 à 5 phrases en français pour évaluer votre niveau…'
    },
    {
      code: 'Anglais',
      label: 'English',
      flag: '🇬🇧',
      placeholder: 'Write 3 to 5 sentences in English to assess your level…'
    },
    {
      code: 'Allemand',
      label: 'Deutsch',
      flag: '🇩🇪',
      placeholder: 'Schreiben Sie 3 bis 5 Sätze auf Deutsch, um Ihr Niveau zu bewerten…'
    },
    {
      code: 'Espagnol',
      label: 'Español',
      flag: '🇪🇸',
      placeholder: 'Escribe de 3 a 5 frases en español para evaluar tu nivel…'
    },
    {
      code: 'Arabe',
      label: 'العربية',
      flag: '🇲🇦',
      placeholder: 'اكتب من 3 إلى 5 جمل باللغة العربية لتقييم مستواك…'
    }
  ];

  selectedLanguage: Language = this.languages[0];
  userText = '';
  isAnalyzing = false;
  result: LanguageDetectResponse | null = null;
  error = '';

  // CEFR level colors and descriptions
  levelConfig: Record<string, { color: string; description: string; icon: string }> = {
    A1: { color: '#e74c3c', description: 'Débutant', icon: 'school' },
    A2: { color: '#e67e22', description: 'Élémentaire', icon: 'menu_book' },
    B1: { color: '#f1c40f', description: 'Intermédiaire', icon: 'auto_stories' },
    B2: { color: '#2ecc71', description: 'Intermédiaire supérieur', icon: 'workspace_premium' },
    C1: { color: '#3498db', description: 'Avancé', icon: 'star' },
    C2: { color: '#9b59b6', description: 'Maîtrise', icon: 'emoji_events' }
  };

  get currentPlaceholder(): string {
    return this.selectedLanguage.placeholder;
  }

  get levelInfo() {
    return this.result ? (this.levelConfig[this.result.level] || this.levelConfig['A1']) : null;
  }

  get scoreWidth(): string {
    return this.result ? `${this.result.score}%` : '0%';
  }

  constructor(private aiService: AiService) {}

  onLanguageChange(lang: Language): void {
    this.selectedLanguage = lang;
    this.result = null;
    this.error = '';
  }

  analyze(): void {
    if (!this.userText.trim() || this.isAnalyzing) return;

    this.isAnalyzing = true;
    this.result = null;
    this.error = '';

    this.aiService.detectLanguageLevel(this.userText, this.selectedLanguage.code).subscribe({
      next: (res) => {
        this.result = res;
        this.isAnalyzing = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Une erreur s\'est produite. Vérifiez que le service AI est démarré.';
        this.isAnalyzing = false;
      }
    });
  }

  reset(): void {
    this.userText = '';
    this.result = null;
    this.error = '';
  }

  getCefrLevels(): string[] {
    return ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];
  }

  isCurrentOrPastLevel(level: string): boolean {
    if (!this.result) return false;
    const levels = this.getCefrLevels();
    return levels.indexOf(level) <= levels.indexOf(this.result.level);
  }
}
