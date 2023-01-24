import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { MessageService } from 'primeng/api';
import { VeznikService } from '../../../services/reci/';
import { TokenStorageService } from '../../../services/auth/token-storage.service';
import { Veznik, toVeznik } from '../../../models/reci';

@Component({
  selector: 'app-veznik',
  templateUrl: './veznik.component.html',
  styleUrls: ['./veznik.component.scss']
})
export class VeznikComponent implements OnInit, AfterViewInit {

  id: number;
  editMode: boolean;
  returnUrl: string;
  sourceWord: string;
  veznik: Veznik;
  @ViewChild('tekst') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private veznikService: VeznikService,
    private titleService: Title
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Везник');
    this.veznik = this.veznikService.new();
    this.route.queryParams.subscribe((params) => {
      this.returnUrl = params.returnUrl;
      this.sourceWord = params.word;
    });
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          this.veznik = { tekst: '', vlasnikID: this.tokenStorageService.getUser().id };
          break;
        case 'edit':
          this.editMode = true;
          this.route.params.subscribe(
            (params) => {
              this.id = +params.id;
              this.veznikService.get(this.id).subscribe({
                next: (item) => {
                  this.veznik = toVeznik(item);
                },
                error: (error) => {
                  console.log(error);
                  this.messageService.add({
                    severity: 'error',
                    summary: 'Грешка',
                    life: 5000,
                    detail: `Везник није учитан: ${error}`,
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

  check(): boolean {
    try {
      this.assert(this.veznik.tekst.trim().length === 0, 'Мора се унети садржај.');
      return true;
    } catch (e) {
      return false;
    }
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
    if (this.editMode) {
      this.veznikService.update({id: this.id, tekst: this.veznik.tekst}).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Везник је успешно сачуван.`,
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
    } else {
      this.veznikService.add({tekst: this.veznik.tekst}).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Везник је успешно сачуван.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
          else
            this.router.navigate(['/veznik', data.id]);
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
    if (this.tokenStorageService.getUser().id === this.veznik?.vlasnikID)
      return true;
    return false;
  }
}
