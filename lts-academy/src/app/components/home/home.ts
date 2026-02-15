import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { FormationService } from '../../services/formation.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, MatCardModule, MatButtonModule, MatIconModule],
  templateUrl: './home.html',
  styleUrls: ['./home.scss']
})
export class Home {
  topFormations;

  constructor(private formationService: FormationService) {
    this.topFormations = this.formationService.getFormations().slice(0, 3);
  }
}
