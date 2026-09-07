import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  history: ChatMessage[];
}

export interface ChatResponse {
  reply: string;
}

export interface LanguageDetectRequest {
  text: string;
  target_language: string;
}

export interface LanguageDetectResponse {
  level: string;
  score: number;
  analysis: string;
  recommendations: string[];
  course_recommendation?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AiService {
  private apiBase = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  chat(message: string, history: ChatMessage[]): Observable<ChatResponse> {
    const payload: ChatRequest = { message, history };
    return this.http.post<ChatResponse>(`${this.apiBase}/chat`, payload);
  }

  detectLanguageLevel(text: string, targetLanguage: string): Observable<LanguageDetectResponse> {
    const payload: LanguageDetectRequest = {
      text,
      target_language: targetLanguage
    };
    return this.http.post<LanguageDetectResponse>(`${this.apiBase}/detect-language`, payload);
  }
}
