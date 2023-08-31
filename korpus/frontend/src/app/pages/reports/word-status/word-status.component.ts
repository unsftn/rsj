import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { DeciderService } from '../../../services/decider/decider.service';

@Component({
  selector: 'app-word-status',
  templateUrl: './word-status.component.html',
  styleUrls: ['./word-status.component.scss']
})
export class WordStatusComponent implements OnInit {

  slova: any[] = [];

  constructor(
      private titleService: Title, 
      private deciderService: DeciderService,
  ) {}

  ngOnInit(): void {
    this.titleService.setTitle('Број унетих речи');
    this.loadStats();
  }

  loadStats(): void {
    this.deciderService.getBrojOdluka().subscribe({
      next: (data: any[]) => this.slova = data,
      error: (error) => console.log(error),
    });
  }
}
