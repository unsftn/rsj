import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FieldsetModule } from 'primeng/fieldset';
import { ChartModule } from 'primeng/chart';
import { TableModule } from 'primeng/table';
import { HomeComponent } from './home.component';
import { RenderedOdredniceComponent } from '../rendered-odrednice/rendered-odrednice.component';

@NgModule({
  declarations: [HomeComponent, RenderedOdredniceComponent],
  imports: [
    CommonModule,
    FieldsetModule,
    ChartModule,
    TableModule,
  ],
  exports: [HomeComponent],
  providers: [],
  bootstrap: [HomeComponent],
})
export class HomeModule {}
