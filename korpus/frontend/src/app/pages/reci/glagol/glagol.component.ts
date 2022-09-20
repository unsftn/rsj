import { Component, OnInit, AfterViewInit, ViewChild, ElementRef} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import {
  Glagol,
  GlagolskaVarijanta,
  GlagolskiRod,
  GlagolskiVid,
  toGlagol
} from '../../../models/reci';
import { GlagolService } from '../../../services/reci';
import { TokenStorageService } from '../../../services/auth/token-storage.service';

@Component({
  selector: 'app-glagol',
  templateUrl: './glagol.component.html',
  styleUrls: ['./glagol.component.scss']
})
export class GlagolComponent implements OnInit, AfterViewInit {

  glagol: Glagol;

  id: number;
  editMode: boolean;
  rodovi: GlagolskiRod[];
  vidovi: GlagolskiVid[];
  varijante: GlagolskaVarijanta[];
  @ViewChild('infinitiv') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private glagolService: GlagolService,
  ) { }

  ngOnInit(): void {
    this.initNew();
    this.rodovi = this.glagolService.getRodovi();
    this.vidovi = this.glagolService.getVidovi();
    this.varijante = this.glagolService.getVarijante();
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          break;
        case 'edit':
          this.editMode = true;
          this.route.params.subscribe(
            (params) => {
              this.id = +params.id;
              this.glagolService.get(this.id).subscribe({
                next: (item) => {
                  this.glagol = toGlagol(item);
                },
                error: (error) => {
                  console.log(error);
                  this.messageService.add({
                    severity: 'error',
                    summary: 'Грешка',
                    life: 5000,
                    detail: 'Глагол није учитан',
                  });
                  this.router.navigate(['/']);
                }
              });
            });
          break;
      }
    });
  }

  ngAfterViewInit(): void {
    this.textInput.nativeElement.focus();
  }

  initNew(): void {
    this.glagol = this.glagolService.new();
  }

  addVarijanta(index: number): void {
    this.glagol.oblici[index].varijante.push({varijanta: null, tekst: ''});
  }

  moveUp(vreme: number, index: number): void {
    if (index === 0)
      return;
    const temp = this.glagol.oblici[vreme].varijante.splice(index, 1)[0];
    this.glagol.oblici[vreme].varijante.splice(index - 1, 0, temp);
  }

  moveDown(vreme: number, index: number): void {
    if (index === this.glagol.oblici[vreme].varijante.length - 1)
      return;
    const temp = this.glagol.oblici[vreme].varijante.splice(index, 1)[0];
    this.glagol.oblici[vreme].varijante.splice(index + 1, 0, temp);
  }

  remove(vreme: number, index: number): void {
    this.glagol.oblici[vreme].varijante.splice(index, 1);
  }

  assert(condition: boolean, message: string): void {
    if (condition) {
      this.messageService.add({
        severity: 'error',
        summary: 'Грешка',
        life: 0,
        detail: message,
      });
      throw new Error();
    }
  }

  check(): boolean {
    try {
      for (const oblik of this.glagol.oblici)
        for (const v of oblik.varijante) {
          this.assert(v.varijanta === null || v.tekst.trim() === '', 'Бар једна варијанта није попуњена.');
        }
      return true;
    } catch (e) {
      return false;
    }
  }

  save(): void {
    if (!this.check()) return;
    console.log('Snimanje glagola:', this.glagol);
    if (!this.editMode) {
      this.glagolService.add(this.glagol).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Глагол је успешно сачуван.`,
          });
          this.router.navigate(['/glagol', data.id]);
        },
        error: (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Грешка',
            life: 5000,
            detail: `Неуспешно снимање: ${error}`,
          });
        }
      });
    } else {
      this.glagolService.update(this.glagol).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Глагол је успешно сачуван.`,
          });
        },
        error: (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Грешка',
            life: 5000,
            detail: `Неуспешно снимање: ${error}`,
          });
        }
      });
    }
  }

  saveAvailable() {
    if (this.tokenStorageService.isEditor())
      return true;
    if (!this.editMode)
      return true;
    if (this.tokenStorageService.getUser().id === this.glagol.vlasnikID)
      return true;
    return false;
  }
}
