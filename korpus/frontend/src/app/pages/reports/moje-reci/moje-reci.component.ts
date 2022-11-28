import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { RecService, StatsService } from '../../../services/reci';
import { TokenStorageService } from '../../../services/auth/token-storage.service';
import { UserService } from '../../../services/auth/user.service';

@Component({
  selector: 'app-moje-reci',
  templateUrl: './moje-reci.component.html',
  styleUrls: ['./moje-reci.component.scss']
})
export class MojeReciComponent implements OnInit {

  mojeReci: any[] = [];
  username: string = '';
  userID: number;

  constructor(
    private router: Router,
    private recService: RecService,
    private statsService: StatsService,
    private activatedRoute: ActivatedRoute,
    private tokenStorageService: TokenStorageService,
    private userService: UserService,
  ) { }

  ngOnInit(): void {
    this.activatedRoute.data.subscribe(data => {
      switch (data.mode) {
        case 'self':
          this.username = (this.tokenStorageService.getUser()?.firstName ?? '') + ' ' + (this.tokenStorageService.getUser()?.lastName ?? '');
          this.userID = null;
          break;
        case 'other':
          this.activatedRoute.params.subscribe(params => {
            this.userID = +params.userID;
            this.userService.getUserInfo(this.userID).subscribe({
              next: (data) => { 
                this.username = data.firstName + ' ' + data.lastName;
              },
              error: (error) => { console.log(error); }
            })
          });
          break;
      }
      this.fetchData();
    });
  }

  fetchData(): void {
    if (!this.userID)
      this.statsService.getMojeReci().subscribe({
        next: (data) => { this.mojeReci = data },
        error: (err) => { console.log(err) }
      });
    else
      this.statsService.getReciKorisnika(this.userID).subscribe({
        next: (data) => { this.mojeReci = data },
        error: (err) => { console.log(err) }
      });
  }

  navigate(rec: any): void {
    this.router.navigate(this.recService.getEditRouterLink(rec.id, rec.vrsta_id));
  }
}
