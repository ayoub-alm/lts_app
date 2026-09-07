import {
  Component,
  OnInit,
  OnDestroy,
  ViewChild,
  ElementRef,
  AfterViewChecked,
  ChangeDetectorRef
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { AiService, ChatMessage } from '../../services/ai.service';
import { Subscription } from 'rxjs';

export interface DisplayMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  loading?: boolean;
}

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule, MatIconModule, MatButtonModule, MatTooltipModule],
  templateUrl: './chatbot.html',
  styleUrls: ['./chatbot.scss']
})
export class ChatbotComponent implements OnInit, OnDestroy, AfterViewChecked {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  isOpen = false;
  userInput = '';
  isTyping = false;
  messages: DisplayMessage[] = [];
  private history: ChatMessage[] = [];
  private subscription?: Subscription;
  private shouldScrollToBottom = false;

  constructor(
    private aiService: AiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    // Initial greeting
    this.messages.push({
      role: 'assistant',
      content: '👋 Bonjour ! Je suis votre conseiller virtuel LTS Academy.\n\nJe peux vous aider à :\n• Découvrir nos formations\n• Choisir votre parcours d\'apprentissage\n• Répondre à vos questions\n\nQue souhaitez-vous savoir ? 😊',
      timestamp: new Date()
    });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  ngAfterViewChecked(): void {
    if (this.shouldScrollToBottom) {
      this.scrollToBottom();
      this.shouldScrollToBottom = false;
    }
  }

  toggleChat(): void {
    this.isOpen = !this.isOpen;
    if (this.isOpen) {
      this.shouldScrollToBottom = true;
    }
  }

  closeChat(): void {
    this.isOpen = false;
  }

  sendMessage(): void {
    const text = this.userInput.trim();
    if (!text || this.isTyping) return;

    // Add user message
    this.messages.push({
      role: 'user',
      content: text,
      timestamp: new Date()
    });

    // Add to history
    this.history.push({ role: 'user', content: text });
    this.userInput = '';
    this.shouldScrollToBottom = true;

    // Show typing indicator
    this.isTyping = true;
    const loadingMsg: DisplayMessage = {
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      loading: true
    };
    this.messages.push(loadingMsg);
    this.shouldScrollToBottom = true;

    this.subscription = this.aiService.chat(text, this.history.slice(0, -1)).subscribe({
      next: (res) => {
        // Replace loading message with actual response
        const idx = this.messages.indexOf(loadingMsg);
        if (idx !== -1) {
          this.messages[idx] = {
            role: 'assistant',
            content: res.reply,
            timestamp: new Date()
          };
        }
        this.history.push({ role: 'assistant', content: res.reply });
        this.isTyping = false;
        this.shouldScrollToBottom = true;
        this.cdr.detectChanges();
      },
      error: (err) => {
        const idx = this.messages.indexOf(loadingMsg);
        if (idx !== -1) {
          this.messages[idx] = {
            role: 'assistant',
            content: '❌ Désolé, une erreur s\'est produite. Veuillez réessayer ou contacter LTS Academy directement au +212 660 356 877.',
            timestamp: new Date()
          };
        }
        this.isTyping = false;
        this.shouldScrollToBottom = true;
        this.cdr.detectChanges();
      }
    });
  }

  onKeyDown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  clearChat(): void {
    this.history = [];
    this.messages = [];
    this.ngOnInit();
  }

  private scrollToBottom(): void {
    try {
      if (this.messagesContainer) {
        const el = this.messagesContainer.nativeElement;
        el.scrollTop = el.scrollHeight;
      }
    } catch {}
  }

  formatContent(content: string): string {
    return content
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>');
  }
}
