import { NgModule } from '@angular/core';
import { FieldsetModule } from 'primeng/fieldset';
import { HomeComponent } from './home.component';
import { RenderedOdredniceComponent } from '../rendered-odrednice/rendered-odrednice.component';

@NgModule({
  declarations: [HomeComponent, RenderedOdredniceComponent],
  imports: [FieldsetModule],
  exports: [HomeComponent],
  providers: [],
  bootstrap: [HomeComponent],
})
export class HomeModule {}
