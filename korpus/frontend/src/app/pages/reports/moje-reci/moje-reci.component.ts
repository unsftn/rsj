import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RecService, StatsService } from '../../../services/reci';

@Component({
  selector: 'app-moje-reci',
  templateUrl: './moje-reci.component.html',
  styleUrls: ['./moje-reci.component.scss']
})
export class MojeReciComponent implements OnInit {

  mojeReci: any[] = [];

  constructor(
    private router: Router,
    private recService: RecService,
    private statsService: StatsService,
  ) { }

  ngOnInit(): void {
    this.fetchData();
  }

  fetchData(): void {
    this.statsService.getMojeReci().subscribe({
      next: (data) => { this.mojeReci = data },
      error: (err) => { console.log(err) }
    });
  }

  navigate(rec: any): void {
    this.router.navigate(this.recService.getEditRouterLink(rec.id, rec.vrsta_id));
  }
}
