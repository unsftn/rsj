import { Component, OnInit } from '@angular/core';
import { StatsService } from '../../../services/reci/stats.service';

@Component({
  selector: 'app-broj-unetih-reci',
  templateUrl: './broj-unetih-reci.component.html',
  styleUrls: ['./broj-unetih-reci.component.scss']
})
export class BrojUnetihReciComponent implements OnInit {

  stats: any[] = [];

  constructor(private statsService: StatsService) { }

  ngOnInit(): void {
    this.loadStats();
  }

  loadStats(): void {
    this.statsService.getBrojUnetihReciZaSve().subscribe({
      next: (data) => { this.stats = data; },
      error: (err) => console.log(err),
    });
  }

}
