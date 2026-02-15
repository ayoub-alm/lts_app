import { Routes } from '@angular/router';
import { Home } from './components/home/home';
import { Poles } from './components/poles/poles';
import { Impact } from './components/impact/impact';
import { FormationDetail } from './components/formation-detail/formation-detail';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'poles', component: Poles },
  { path: 'impact', component: Impact },
  { path: 'formations/:id', component: FormationDetail },
  { path: '**', redirectTo: '' }
];
