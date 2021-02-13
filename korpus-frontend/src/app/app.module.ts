import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { AuthInterceptor } from './services/auth/auth.interceptor';
import { ErrorInterceptor } from './services/auth/error.interceptor';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { MenubarModule } from 'primeng/menubar';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { TieredMenuModule } from 'primeng/tieredmenu';
import { FieldsetModule } from 'primeng/fieldset';
import { TabViewModule } from 'primeng/tabview';
import { ToastModule } from 'primeng/toast';
import { ScrollTopModule } from 'primeng/scrolltop';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { CheckboxModule } from 'primeng/checkbox';
import { TooltipModule } from 'primeng/tooltip';
import { DropdownModule } from 'primeng/dropdown';
import { ToolbarModule } from 'primeng/toolbar';
import { RadioButtonModule } from 'primeng/radiobutton';
import { HomeModule } from './components/home/home.module';
import { SelectWordComponent } from './components/select-word/select-word.component';
import { FormSelectorComponent } from './components/form-selector/form-selector.component';
import { ImenicaComponent } from './components/imenica/imenica.component';
import { GlagolComponent } from './components/glagol/glagol.component';
import { PridevComponent } from './components/pridev/pridev.component';
import { LoginComponent } from './components/login/login.component';

@NgModule({
  declarations: [
    AppComponent,
    SelectWordComponent,
    FormSelectorComponent,
    ImenicaComponent,
    GlagolComponent,
    PridevComponent,
    LoginComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    AppRoutingModule,
    MenubarModule,
    InputTextModule,
    ButtonModule,
    TieredMenuModule,
    FieldsetModule,
    TabViewModule,
    ToastModule,
    ScrollTopModule,
    OverlayPanelModule,
    CheckboxModule,
    TooltipModule,
    DropdownModule,
    ToolbarModule,
    RadioButtonModule,
    HomeModule
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
