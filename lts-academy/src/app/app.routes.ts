import { Routes } from '@angular/router';
import { Home } from './components/home/home';
import { Poles } from './components/poles/poles';
import { Impact } from './components/impact/impact';
import { ImpactEnvironnement } from './components/impact-environnement/impact-environnement';
import { FormationDetail } from './components/formation-detail/formation-detail';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'poles', component: Poles },
  { path: 'impact', component: Impact },
  { path: 'impact-environnement', component: ImpactEnvironnement },
  { path: 'formations/:id', component: FormationDetail },
  { path: '**', redirectTo: '' }
];
