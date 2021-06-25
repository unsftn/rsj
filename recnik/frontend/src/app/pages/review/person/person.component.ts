import { Component, HostListener, OnInit } from '@angular/core';
import { DomSanitizer, Title } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { UserService } from '../../../services/auth/user.service';
import { EnumService, OdrednicaService } from '../../../services/odrednice';

@Component({
  selector: 'app-person',
  templateUrl: './person.component.html',
  styleUrls: ['./person.component.scss']
})
export class PersonComponent implements OnInit {

  obradjivaci: any[] = [];
  selected: any = {};
  odrednice: any[] = [];

  constructor(
    private userService: UserService,
    private router: Router,
    private odrednicaService: OdrednicaService,
    private enumService: EnumService,
    private titleService: Title) { }

  ngOnInit(): void {
    this.titleService.setTitle('Преглед по обрађивачу');
    this.obradjivaci = this.userService.getObradjivaci();
  }

  showUser(user: any): void {
    this.selected = user;
    this.odrednicaService.odredniceObradjivaca(user.id).subscribe(
      (data) => {
        this.odrednice = data;
        this.odrednice.forEach(item => {
          item.stanjeStr = this.enumService.getEntryState(item.stanje).opis;
          item.vrstaStr = this.enumService.getWordType(item.vrsta).name;
        });
      },
      (error) => console.log(error)
    );
  }

  open(odrednicaId: number): void {
    const url = this.router.serializeUrl(this.router.createUrlTree([`/edit/${odrednicaId}`]));
    window.open(url, '_blank');
  }
}
