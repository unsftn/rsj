import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Zamenica, toZamenica } from '../../../models/reci';
import { ZamenicaService } from '../../../services/reci';
import { TokenStorageService } from '../../../services/auth/token-storage.service';

@Component({
  selector: 'app-zamenica',
  templateUrl: './zamenica.component.html',
  styleUrls: ['./zamenica.component.scss']
})
export class ZamenicaComponent implements OnInit, AfterViewInit {

  zamenica: Zamenica;

  id: number;
  editMode: boolean;
  returnUrl: string;
  sourceWord: string;
  @ViewChild('nomjed') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private zamenicaService: ZamenicaService,
  ) { }

  ngOnInit(): void {
    this.initNew();
    this.route.queryParams.subscribe((params) => {
      this.returnUrl = params.returnUrl;
      this.sourceWord = params.word;
    });
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
              this.zamenicaService.get(this.id).subscribe({
                next: (item) => {
                  this.zamenica = toZamenica(item);
                },
                error: (error) => {
                  console.log(error);
                  this.messageService.add({
                    severity: 'error',
                    summary: 'Грешка',
                    life: 5000,
                    detail: 'Именица није учитана',
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
    this.zamenica = this.zamenicaService.new();
  }

  check(): boolean {
    try {
      this.assert(this.zamenica.nomjed.trim().length === 0, 'Мора се унети номинатив једнине.');
      return true;
    } catch (e) {
      return false;
    }
  }

  addVarijanta(): void {
    const rbr = this.zamenica.varijante.length;
    this.zamenica.varijante.push({ redni_broj: rbr + 1, nomjed: '', genjed: '', datjed: '', akujed: '', vokjed: '', insjed: '', lokjed: '' });
    setTimeout(() => {
      document.getElementById(`nomjed${this.zamenica.varijante.length - 1}`).focus();
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
    console.log('Snimanje zamenice:', this.zamenica);
    if (!this.editMode) {
      this.zamenicaService.add(this.zamenica).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Заменица је успешно сачувана.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
          else
            this.router.navigate(['/zamenica', data.id]);
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
      this.zamenicaService.update(this.zamenica).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Заменица је успешно сачувана.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
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

  moveUp(index: number): void {
    if (index === 0)
      return;
    const temp = this.zamenica.varijante.splice(index, 1)[0];
    this.zamenica.varijante.splice(index - 1, 0, temp);
  }

  moveDown(index: number): void {
    if (index === this.zamenica.varijante.length - 1)
      return;
    const temp = this.zamenica.varijante.splice(index, 1)[0];
    this.zamenica.varijante.splice(index + 1, 0, temp);
  }

  remove(index: number): void {
    this.zamenica.varijante.splice(index, 1);
  }

  saveAvailable() {
    if (this.tokenStorageService.isEditor())
      return true;
    if (!this.editMode)
      return true;
    if (this.tokenStorageService.getUser().id === this.zamenica.vlasnikID)
      return true;
    return false;
  }
}
