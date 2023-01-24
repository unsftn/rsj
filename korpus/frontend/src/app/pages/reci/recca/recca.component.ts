import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';
import { MessageService } from 'primeng/api';
import { ReccaService } from '../../../services/reci/';
import { TokenStorageService } from '../../../services/auth/token-storage.service';
import { Recca, toRecca } from '../../../models/reci';

@Component({
  selector: 'app-recca',
  templateUrl: './recca.component.html',
  styleUrls: ['./recca.component.scss']
})
export class ReccaComponent implements OnInit {

  id: number;
  editMode: boolean;
  returnUrl: string;
  sourceWord: string;
  recca: Recca;
  @ViewChild('tekst') textInput!: ElementRef<HTMLInputElement>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private tokenStorageService: TokenStorageService,
    private reccaService: ReccaService,
    private titleService: Title
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Речца');
    this.recca = this.reccaService.new();
    this.route.queryParams.subscribe((params) => {
      this.returnUrl = params.returnUrl;
      this.sourceWord = params.word;
    });
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.editMode = false;
          this.recca = { tekst: '', vlasnikID: this.tokenStorageService.getUser().id };
          setTimeout(() => this.textInput.nativeElement.focus(), 1);
          break;
        case 'edit':
          this.editMode = true;
          this.route.params.subscribe(
            (params) => {
              this.id = +params.id;
              this.reccaService.get(this.id).subscribe({
                next: (item) => {
                  this.recca = toRecca(item);
                  setTimeout(() => this.textInput.nativeElement.focus(), 1);
                },
                error: (error) => {
                  console.log(error);
                  this.messageService.add({
                    severity: 'error',
                    summary: 'Грешка',
                    life: 5000,
                    detail: `Речца није учитана: ${error}`,
                  });
                  this.router.navigate(['/']);
                }
            });
          });
          break;        
      }
    });
  }

  check(): boolean {
    try {
      this.assert(this.recca.tekst.trim().length === 0, 'Мора се унети садржај.');
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
      this.reccaService.update({id: this.id, tekst: this.recca.tekst}).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Речца је успешно сачувана.`,
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
      this.reccaService.add({tekst: this.recca.tekst}).subscribe({
        next: (data) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Успех',
            life: 3000,
            detail: `Речца је успешно сачувана.`,
          });
          if (this.returnUrl)
            this.router.navigate([this.returnUrl]);
          else
            this.router.navigate(['/recca', data.id]);
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
    if (this.tokenStorageService.getUser().id === this.recca?.vlasnikID)
      return true;
    return false;
  }
}
