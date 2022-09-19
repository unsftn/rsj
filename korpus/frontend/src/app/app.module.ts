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
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { PaginatorModule } from 'primeng/paginator';
import { NgParticlesModule } from 'ng-particles';

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
import { ProfileComponent } from './pages/profile/profile.component';
import { SafePipe } from './utils/safe.pipe';
import { ReccaComponent } from './pages/reci/recca/recca.component';
import { UzvikComponent } from './pages/reci/uzvik/uzvik.component';
import { VeznikComponent } from './pages/reci/veznik/veznik.component';
import { PredlogComponent } from './pages/reci/predlog/predlog.component';
import { PrilogComponent } from './pages/reci/prilog/prilog.component';
import { BrojComponent } from './pages/reci/broj/broj.component';
import { ZamenicaComponent } from './pages/reci/zamenica/zamenica.component';
import { AdvancedSearchComponent } from './pages/advanced-search/advanced-search.component';
import { AllWordsComponent } from './pages/reports/all-words/all-words.component';
import { BrojUnetihReciComponent } from './pages/reports/broj-unetih-reci/broj-unetih-reci.component';
import { MojeReciComponent } from './pages/reports/moje-reci/moje-reci.component';

@NgModule({
  declarations: [AppComponent, LoginComponent, HomeComponent, ImenicaComponent, ToolbarComponent, GlagolComponent, PridevComponent, PublicationComponent, PubTextComponent, PubListComponent, ProfileComponent, SafePipe, ReccaComponent, UzvikComponent, VeznikComponent, PredlogComponent, PrilogComponent, BrojComponent, ZamenicaComponent, AdvancedSearchComponent, AllWordsComponent, BrojUnetihReciComponent, MojeReciComponent],
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
    PaginatorModule,
    NgParticlesModule,
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
