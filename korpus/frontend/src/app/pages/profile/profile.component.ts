import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ValidationErrors, Validators } from '@angular/forms';
import { Title } from '@angular/platform-browser';
import { TokenStorageService } from '../../services/auth/token-storage.service';
import { AuthService } from '../../services/auth/auth.service';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {

  user: any;
  changePass = false;
  changePassForm: FormGroup;
  submitted = false;

  constructor(
    private tokenStorageService: TokenStorageService,
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private messageService: MessageService,
    private titleService: Title) { }

  ngOnInit(): void {
    this.titleService.setTitle('Профил');
    this.user = this.tokenStorageService.getUser();
    console.log(this.user);
    this.changePassForm = this.formBuilder.group({
      lozinka1: ['', [Validators.required]],
      lozinka2: ['', [Validators.required]],
    }, {validators: [this.passwordsMatchValidator]} );
  }

  get f() {
    return this.changePassForm.controls;
  }

  passwordsMatchValidator(fg: FormGroup): ValidationErrors | null {
    const p1 = fg.get('lozinka1').value;
    const p2 = fg.get('lozinka2').value;
    if (!p1 || !p2)
      return null;
    // this.changePassForm.controls['lozinka2'].setErrors({password: true});
    return (p1 === p2) ? null : { mismatch: true };
  }

  onSubmit(): void {
    this.submitted = true;
    this.authService.changePassword(this.f.lozinka1.value).subscribe(
      (data) => {
        this.messageService.add({
          severity: 'success',
          summary: 'Успешна промена',
          life: 5000,
          detail: 'Лозинка је успешно промењена.',
        });
        this.submitted = false;
        this.changePass = false;
      },
      (error) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: 'Промена лозинке је неуспешна.',
        });
        this.submitted = false;
        this.changePass = false;
      });
  }

}
