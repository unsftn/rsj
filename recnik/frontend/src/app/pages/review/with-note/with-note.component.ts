import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { EnumService, OdrednicaService } from '../../../services/odrednice';

@Component({
  selector: 'app-with-note',
  templateUrl: './with-note.component.html',
  styleUrls: ['./with-note.component.scss']
})
export class WithNoteComponent implements OnInit {

  odrednice: any[] = [];

  constructor(
    private router: Router,
    private odrednicaService: OdrednicaService,
    private enumService: EnumService,
    private titleService: Title) { }

  ngOnInit(): void {
    this.titleService.setTitle('Oдреднице са напоменом');
    this.odrednicaService.getAllWithNotes().subscribe(data => {
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
