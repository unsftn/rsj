import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FieldsetModule } from 'primeng/fieldset';
import { HomeComponent } from './home.component';
import { RenderedOdredniceComponent } from '../rendered-odrednice/rendered-odrednice.component';

@NgModule({
  declarations: [HomeComponent, RenderedOdredniceComponent],
  imports: [FieldsetModule, HttpClientModule, FormsModule],
  exports: [HomeComponent],
  providers: [],
  bootstrap: [HomeComponent],
})
export class HomeModule {}
