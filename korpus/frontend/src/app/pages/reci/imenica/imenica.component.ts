import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Imenica, toImenica, VrstaImenice } from '../../../models/reci';
import { ImenicaService } from '../../../services/reci';

@Component({
  selector: 'app-imenica',
  templateUrl: './imenica.component.html',
  styleUrls: ['./imenica.component.scss']
})
export class ImenicaComponent implements OnInit {

  imenica: Imenica;

  id: number;
  editMode: boolean;
  vrste: VrstaImenice[];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private imenicaService: ImenicaService,
  ) { }

  ngOnInit(): void {
    this.initNew();
    this.vrste = this.imenicaService.getVrste();
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          document.getElementById('nomjed').focus();
          break;
        case 'edit':
          this.editMode = true;
          this.route.params.subscribe(
            (params) => {
              this.id = +params.id;
              this.imenicaService.get(this.id).subscribe((item) => {
                this.imenica = toImenica(item);
              },
              (error) => {
                console.log(error);
                this.messageService.add({
                  severity: 'error',
                  summary: 'Грешка',
                  life: 5000,
                  detail: 'Именица није учитана',
                });
                this.router.navigate(['/']);
              });
            });
          break;
      }
    });
  }

  initNew(): void {
    this.imenica = this.imenicaService.new();
  }

  check(): boolean {
    try {
      this.assert(this.imenica.nomjed.trim().length === 0, 'Мора се унети номинатив једнине.');
      return true;
    } catch (e) {
      return false;
    }
  }

  addVarijanta(): void {
    const rbr = this.imenica.varijante.length;
    this.imenica.varijante.push({ redni_broj: rbr, nomjed: '', genjed: '', datjed: '', akujed: '', vokjed: '', insjed: '', lokjed: '', nommno: '', genmno: '', datmno: '', akumno: '', vokmno: '', insmno: '', lokmno: ''});
    setTimeout(() => {
      document.getElementById(`nomjed${this.imenica.varijante.length - 1}`).focus();
      scrollTo(0, document.body.scrollHeight);
    });
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

  save(): void {
    if (!this.check()) return;
    console.log('Snimanje imenice:', this.imenica);
    if (!this.editMode) {
      this.imenicaService.add(this.imenica).subscribe(
        (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Именица је успешно сачувана.`,
          });
          this.router.navigate(['/imenica', data.id]);
        },
        (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Грешка',
            life: 5000,
            detail: `Неуспешно снимање: ${error}`,
          });
        });
    } else {
      this.imenicaService.update(this.imenica).subscribe(
        (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Именица је успешно сачувана.`,
          });
        },
        (error) => {
          this.messageService.add({
            severity: 'error',
            summary: 'Грешка',
            life: 5000,
            detail: `Неуспешно снимање: ${error}`,
          });
        });
    }
  }

  moveUp(index: number): void {
    if (index === 0)
      return;
    const temp = this.imenica.varijante.splice(index, 1)[0];
    this.imenica.varijante.splice(index - 1, 0, temp);
  }

  moveDown(index: number): void {
    if (index === this.imenica.varijante.length - 1)
      return;
    const temp = this.imenica.varijante.splice(index, 1)[0];
    this.imenica.varijante.splice(index + 1, 0, temp);
  }

  remove(index: number): void {
    this.imenica.varijante.splice(index, 1);
  }
}
