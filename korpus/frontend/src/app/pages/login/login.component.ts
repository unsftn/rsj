import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';
import { TokenStorageService } from '../../services/auth/token-storage.service';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  returnUrl: string;
  submitted = false;
  loading = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private tokenStorage: TokenStorageService,
    private messageService: MessageService
  ) {}

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      username: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });
    this.returnUrl = this.route.snapshot.queryParams.returnUrl || '/';
  }

  get f() {
    return this.loginForm.controls;
  }

  onSubmit(): void {
    this.submitted = true;
    if (this.loginForm.invalid) {
      return;
    }
    this.loading = true;

    const email = this.f.username.value.trim();
    const password = this.f.password.value.trim();
    this.authService.login(email, password).subscribe({
      next: (data) => {
        this.tokenStorage.saveToken(data.access, data.refresh);
        this.tokenStorage.saveUser({ email, password, firstName: data.first_name, lastName: data.last_name, isStaff: data.is_staff, groups: data.groups});
        this.router.navigate([this.returnUrl]);
      },
      error: (err) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: 'Неуспешно пријављивање: неисправна адреса е-поште и/или лозинка.',
        });
      },
    });
  }

  forgotPassword(): void {
    const email = this.f.username.value.trim();
    this.authService.forgotPassword(email).subscribe({
      next: (data) => {
        this.messageService.add({
          severity: 'success',
          summary: 'Послат и-мејл',
          life: 5000,
          detail: 'На Вашу и-мејл адресу је послатa нова лозинка.'
        });
      },
      error: (еrror) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: 'Корисник са датом и-мејл адресом није познат.'
        });
      }
    });
  }
}
