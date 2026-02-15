import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { FormationService } from '../../services/formation.service';

@Component({
  selector: 'app-poles',
  standalone: true,
  imports: [CommonModule, RouterModule, MatCardModule, MatButtonModule],
  templateUrl: './poles.html',
  styleUrls: ['./poles.scss']
})
export class Poles {
  formations;

  constructor(private formationService: FormationService) {
    this.formations = this.formationService.getFormations();
  }
}
