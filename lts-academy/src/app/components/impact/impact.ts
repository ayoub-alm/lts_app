import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-impact',
  standalone: true,
  imports: [CommonModule, MatCardModule],
  templateUrl: './impact.html',
  styleUrls: ['./impact.scss']
})
export class Impact {}
