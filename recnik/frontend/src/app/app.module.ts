import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';

import { AuthInterceptor } from './services/auth/auth.interceptor';
import { AuthErrorInterceptor } from './services/auth/auth-error.interceptor.service';
import { ErrorInterceptor } from './services/error';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MenubarModule } from 'primeng/menubar';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { TieredMenuModule } from 'primeng/tieredmenu';
import { FieldsetModule } from 'primeng/fieldset';
import { TabViewModule } from 'primeng/tabview';
import { ToastModule } from 'primeng/toast';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { TableModule } from 'primeng/table';
import { ToolbarModule } from 'primeng/toolbar';
import { MenuModule } from 'primeng/menu';
import { DialogModule } from 'primeng/dialog';
import { DropdownModule } from 'primeng/dropdown';
import { ToggleButtonModule } from 'primeng/togglebutton';
import { PasswordModule } from 'primeng/password';

// import { HomeModule } from './pages/home/home.module';
import { TabFormModule } from './pages/tabForm/tabForm.module';
import { PublikacijaComponent } from './pages/publikacije/publikacija/publikacija.component';
import { LoginComponent } from './pages/login/login.component';
import { RendersComponent } from './pages/renders/renders/renders.component';
import { PublikacijaListComponent } from './pages/publikacije/publikacija-list/publikacija-list.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { PersonComponent } from './pages/review/person/person.component';
import { RenderedOdredniceComponent } from './pages/rendered-odrednice/rendered-odrednice.component';
import { HomeComponent } from './pages/home/home.component';
import { AllComponent } from './pages/review/all/all.component';

@NgModule({
  declarations: [AppComponent, LoginComponent, RendersComponent, PublikacijaComponent, PublikacijaListComponent,
    ProfileComponent, PersonComponent, RenderedOdredniceComponent, HomeComponent, AllComponent],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    MenubarModule,
    InputTextModule,
    ButtonModule,
    TieredMenuModule,
    FieldsetModule,
    TabViewModule,
    TabFormModule,
    ToastModule,
    //HomeModule,
    AutoCompleteModule,
    TableModule,
    ToolbarModule,
    MenuModule,
    DialogModule,
    DropdownModule,
    ToggleButtonModule,
    PasswordModule,
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: AuthErrorInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
  ],
  bootstrap: [AppComponent],
  exports: [],
})
export class AppModule {}
