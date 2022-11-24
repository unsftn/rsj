import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { RecService, StatsService } from '../../../services/reci';
import { TokenStorageService } from '../../../services/auth/token-storage.service';

@Component({
  selector: 'app-moje-reci',
  templateUrl: './moje-reci.component.html',
  styleUrls: ['./moje-reci.component.scss']
})
export class MojeReciComponent implements OnInit {

  mojeReci: any[] = [];
  username: string = '';

  constructor(
    private router: Router,
    private recService: RecService,
    private statsService: StatsService,
    private tokenStorageService: TokenStorageService,
  ) { }

  ngOnInit(): void {
    this.username = (this.tokenStorageService.getUser()?.firstName ?? '') + ' ' + (this.tokenStorageService.getUser()?.lastName ?? '');
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
