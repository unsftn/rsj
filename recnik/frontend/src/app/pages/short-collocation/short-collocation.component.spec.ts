import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShortCollocationComponent } from './short-collocation.component';

describe('ShortCollocationComponent', () => {
  let component: ShortCollocationComponent;
  let fixture: ComponentFixture<ShortCollocationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShortCollocationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ShortCollocationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
