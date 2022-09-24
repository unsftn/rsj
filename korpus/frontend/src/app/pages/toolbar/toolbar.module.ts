import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { ToolbarModule } from 'primeng/toolbar';
import { NgParticlesModule } from 'ng-particles';
import { ToolbarComponent } from './toolbar.component';

@NgModule({
  declarations: [ToolbarComponent],
  imports: [
    CommonModule,
    ButtonModule,
    ToolbarModule,
    NgParticlesModule,
  ],
  exports: [ToolbarComponent]
})
export class MyToolbarModule { }
