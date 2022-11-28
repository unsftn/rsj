import { Component, OnInit } from '@angular/core';
import { StatsService } from '../../../services/reci/stats.service';
import { TokenStorageService } from '../../../services/auth/token-storage.service';

@Component({
  selector: 'app-broj-unetih-reci',
  templateUrl: './broj-unetih-reci.component.html',
  styleUrls: ['./broj-unetih-reci.component.scss']
})
export class BrojUnetihReciComponent implements OnInit {

  stats: any[] = [];
  isAdmin: boolean = false;

  constructor(
    private statsService: StatsService,
    private tokenStorageService: TokenStorageService,
  ) { }

  ngOnInit(): void {
    this.isAdmin = this.tokenStorageService.getUser().isStaff;
    this.loadStats();
  }

  loadStats(): void {
    this.statsService.getBrojUnetihReciZaSve().subscribe({
      next: (data) => { this.stats = data; },
      error: (err) => console.log(err),
    });
  }

}
