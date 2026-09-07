import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-impact',
  standalone: true,
  imports: [CommonModule, RouterModule, MatCardModule],
  templateUrl: './impact.html',
  styleUrls: ['./impact.scss']
})
export class Impact {}
