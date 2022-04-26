import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HTTP_INTERCEPTORS, HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { ListboxModule } from 'primeng/listbox';
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
import { ChartModule } from 'primeng/chart';
import { RippleModule } from 'primeng/ripple';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { CheckboxModule } from 'primeng/checkbox';
import { TimelineModule } from 'primeng/timeline';
import { CardModule } from 'primeng/card';
import { OrderListModule } from 'primeng/orderlist';
import { FileUploadModule } from 'primeng/fileupload';
import { AccordionModule } from 'primeng/accordion';

import { AuthInterceptor } from './services/auth/auth.interceptor';
import { AuthErrorInterceptor } from './services/auth/auth-error.interceptor.service';
import { ErrorInterceptor } from './services/error';

import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { LoginComponent } from './pages/login/login.component';
import { HomeComponent } from './pages/home/home.component';
import { ImenicaComponent } from './pages/reci/imenica/imenica.component';
import { ToolbarComponent } from './pages/toolbar/toolbar.component';
import { GlagolComponent } from './pages/reci/glagol/glagol.component';
import { PridevComponent } from './pages/reci/pridev/pridev.component';
import { PublicationComponent } from './pages/publication/publication.component';
import { PubTextComponent } from './pages/pub-text/pub-text.component';
import { PubListComponent } from './pages/pub-list/pub-list.component';
import { SafePipe } from './utils/safe.pipe';
import { ProgressSpinnerModule } from 'primeng/progressspinner';

@NgModule({
  declarations: [AppComponent, LoginComponent, HomeComponent, ImenicaComponent, ToolbarComponent, GlagolComponent, PridevComponent, PublicationComponent, PubTextComponent, PubListComponent, SafePipe],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({cookieName: 'csrftoken', headerName: 'X-CSRFToken',}),
    MenubarModule,
    InputTextModule,
    ButtonModule,
    TieredMenuModule,
    FieldsetModule,
    TabViewModule,
    ToastModule,
    AutoCompleteModule,
    TableModule,
    ToolbarModule,
    MenuModule,
    DialogModule,
    DropdownModule,
    ToggleButtonModule,
    PasswordModule,
    ChartModule,
    ListboxModule,
    RippleModule,
    OverlayPanelModule,
    CheckboxModule,
    TimelineModule,
    CardModule,
    OrderListModule,
    FileUploadModule,
    AccordionModule,
    ProgressSpinnerModule,
    // ImporterModule,
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
