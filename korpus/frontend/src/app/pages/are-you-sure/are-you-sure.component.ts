import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { RecService } from '../../services/reci';

@Component({
  selector: 'are-you-sure',
  templateUrl: './are-you-sure.component.html',
  styleUrls: ['./are-you-sure.component.scss']
})
export class AreYouSureComponent implements OnInit {

  @Input() visible: boolean;
  @Input() message: string;
  @Output() yes: EventEmitter<boolean> = new EventEmitter<boolean>();
  @Output() no: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor(private recService: RecService) {
    this.visible = false;
    this.message = '';
  }

  ngOnInit(): void {
  }

  yesClicked(): void {
    this.yes.emit(true);
    this.visible = true;
  }

  noClicked(): void {
    this.no.emit(true);
    this.visible = false;
  }

}
