import { Component, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { EnumService, OdrednicaService } from '../../../services/odrednice';

@Component({
  selector: 'app-all',
  templateUrl: './all.component.html',
  styleUrls: ['./all.component.scss']
})
export class AllComponent implements OnInit {

  odrednice: any[] = [];

  constructor(
    private router: Router,
    private odrednicaService: OdrednicaService,
    private enumService: EnumService) { }

  ngOnInit(): void {
    this.odrednicaService.getAllSorted().subscribe(data => {
        this.odrednice = data;
        this.odrednice.forEach(item => {
          item.stanjeStr = this.enumService.getEntryState(item.stanje).opis;
          item.vrstaStr = this.enumService.getWordType(item.vrsta).name;
        });
      },
      error => console.log(error)
    );
  }

  open(odrednicaId: number): void {
    const url = this.router.serializeUrl(this.router.createUrlTree([`/edit/${odrednicaId}`]));
    window.open(url, '_blank');
  }
}
