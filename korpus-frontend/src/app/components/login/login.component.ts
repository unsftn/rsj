import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';
import { TokenStorageService } from '../../services/auth/token-storage.service';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  loginForm: FormGroup;
  returnUrl: string;

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

  get form() {
    return this.loginForm.controls;
  }

  onSubmit(): void {
    if (this.loginForm.invalid)
      return;
    const email = this.form.username.value.trim();
    const password = this.form.password.value.trim();
    this.authService.login(email, password).subscribe(
      (data) => {
        this.tokenStorage.saveToken(data.access, data.refresh);
        this.tokenStorage.saveUser({ email, password });
        this.router.navigate([this.returnUrl]);
      },
      (err) => {
        /*this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: 'Неуспешно пријављивање: неисправна имејл адреса и/или лозинка.'
        });*/
        this.messageService.add({
          severity: 'info',
          summary: 'Обавештење',
          life: 5000,
          detail: 'Пријава још није имплементирана'
        });
        this.router.navigate([this.returnUrl]); // delete when login is implemented
      },
    );
  }
}
