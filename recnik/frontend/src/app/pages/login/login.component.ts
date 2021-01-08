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
      console.log('invalid');
      console.log(this.f.username.value);
      console.log(this.f.password.value);
      return;
    }
    this.loading = true;

    const email = this.f.username.value.trim();
    const password = this.f.password.value.trim();
    this.authService.login(email, password).subscribe(
      (data) => {
        this.tokenStorage.saveToken(data.access, data.refresh);
        this.tokenStorage.saveUser({ email, password });
        this.router.navigate([this.returnUrl]);
      },
      (err) => {
        console.log(err);
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: 'Неуспешно пријављивање: неисправна адреса е-поште и/или лозинка.',
        });
      },
    );
  }
}
