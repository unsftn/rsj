import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { MenuItem, PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.scss']
})
export class ToolbarComponent implements OnInit {

  workflowItems: MenuItem[];
  @Input() title = '';
  @Output() saveClicked = new EventEmitter();

  constructor(
    private primengConfig: PrimeNGConfig) { }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }

  undoAvailable(): boolean {
    return true;
  }

  redoAvailable(): boolean {
    return true;
  }

  workflowDisabled(): boolean {
    return false;
  }

  undo(): void {
  }

  redo(): void {
  }

  preview(): void {
  }

  save(): void {
    this.saveClicked.emit();
  }

  delete(): void {
  }
}
