import { Injectable } from '@angular/core';
import formationsData from './formations.json';

export interface Formation {
  id: string;
  title: string;
  subtitle: string;
  image: string;
  presentation: string;
  program: Array<{ title: string; description: string }>;
  opportunities: string[];
}

@Injectable({
  providedIn: 'root'
})
export class FormationService {
  private formations: Formation[] = formationsData as any;

  constructor() { }

  getFormations(): Formation[] {
    return this.formations;
  }

  getFormationById(id: string): Formation | undefined {
    return this.formations.find(f => f.id === id);
  }
}
